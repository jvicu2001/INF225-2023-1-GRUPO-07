from fastapi import APIRouter, File, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

import aiofiles
import aiohttp

import rasterio

import motor.motor_asyncio

import os
import uuid

from jose import jwt

from hashlib import md5

from fastapi.encoders import jsonable_encoder

from models import FileMetadataModel, GeoTiffMetadataModel

client = motor.motor_asyncio.AsyncIOMotorClient(f'{os.environ["MONGODB_URL"]}')

SECRET_KEY = open("/run/secrets/oauth-secret", "r").read()

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def upload_file(file: UploadFile, dataType: int, token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/token"))):
    # DEM:0, DTM:1, DSM:2
    if dataType not in [0,1,2]:
        return JSONResponse(content={'error': 'El tipo de archivo no es válido'}, status_code=status.HTTP_400_BAD_REQUEST)

    if file.content_type == 'image/tiff':
        # Creamos una carpeta con nombre único
        folder = str(uuid.uuid4())
        os.makedirs(f'/data/files/{folder}', exist_ok=True)

        file_path = f'/data/files/{folder}/{file.filename}'

        # Guardamos el archivo en la carpeta
        async with aiofiles.open(file_path, 'wb') as f:
            while content := await file.read(1024):
                await f.write(content)

        # Calculamos el hash md5 del archivo
        hashstring: str = ""
        async with aiofiles.open(file_path, 'rb') as f:
            hash = md5()
            while content := await f.read(1024):
                hash.update(content)
            hashstring = hash.hexdigest()

        # Verificamos que el archivo no exista en la base de datos
        db = client.Files
        if await db["Files"].find_one({"hash": hashstring}) is not None:
            
            # Eliminamos el archivo (este ya se encuentra en otra carpeta)
            os.remove(file_path)
            os.rmdir(f'/data/files/{folder}')

            # Retornamos error de conflicto (código 409)
            return JSONResponse(content={'error': 'El archivo ya existe'}, status_code=status.HTTP_409_CONFLICT)

        # Registramos el archivo en la base de datos
        new_file = await db["Files"].insert_one({
            "filename": file.filename,
            "folder": folder,
            "path": file_path,
            "hash": hashstring
        })

        # Obtenemos el nombre del usuario que subió el archivo mediante el token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = decoded_token.get("username")

        if username is None or file.filename is None:
            # Si el token no contiene un nombre de usuario, o el archivo no tiene nombre, eliminamos el archivo y retornamos un error
            os.remove(file_path)
            os.rmdir(f'/data/files/{folder}')

            # Borrar entrada de la base de datos
            await db["Files"].delete_one({"_id": new_file.inserted_id})

            return JSONResponse(content={'error': 'El token no es válido'}, status_code=status.HTTP_401_UNAUTHORIZED)

        # Abrimos el archivo con rasterio
        with rasterio.open(file_path) as dataset:
            # Obtenemos los metadatos
            filedata: GeoTiffMetadataModel = GeoTiffMetadataModel(
                count=dataset.count,
                crs=dataset.crs.to_string(),
                dtype=dataset.dtypes[0],
                driver=dataset.driver,
                bounds=list(dataset.bounds),
                lnglat=list(dataset.lnglat()),
                height=dataset.height,
                width=dataset.width,
                shape=list(dataset.shape),
                res=list(dataset.res),
                nodata=(dataset.nodata if dataset.nodata is not None else 0.0),
                tags=dataset.tags(),
            )

            metadata: FileMetadataModel = FileMetadataModel(
                fileData=filedata,
                user=username,
                fileName=file.filename,
                fileDataType=dataType,
                fileId=new_file.inserted_id.__str__()
            )          

            # Convertimos los metadatos a JSON
            metadata = jsonable_encoder(metadata)

            # Enviamos estos datos al microservicio de metadatos
            async with aiohttp.ClientSession() as session:
                headers = jsonable_encoder({'accept': 'application/json', 'Authorization': f'Bearer {token}'})

                async with session.post('http://metadata:8010/metadata/', json=metadata, headers=headers) as response:
                    if response.status != 201:
                        # Si el microservicio de metadatos retorna un error, eliminamos el archivo y retornamos el error
                        os.remove(file_path)
                        os.rmdir(f'/data/files/{folder}')

                        # Borrar entrada de la base de datos
                        await db["Files"].delete_one({"_id": new_file.inserted_id})

                        return JSONResponse(content=await response.json(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return JSONResponse(content=await response.json(), status_code=status.HTTP_201_CREATED)

    # Si el archivo no es de tipo GeoTiff
    else:
        return JSONResponse(content={'error': 'El archivo no es de tipo GeoTiff'}, status_code=status.HTTP_400_BAD_REQUEST)