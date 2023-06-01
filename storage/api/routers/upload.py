from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

import aiofiles
import aiohttp

import rasterio

import motor.motor_asyncio

import os
import uuid

from hashlib import md5

from fastapi.encoders import jsonable_encoder

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_FILEAPI_URL"])

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def upload_file(file: UploadFile):
    if file.content_type == 'image/tiff':
        # Creamos una carpeta con nombre único
        folder = str(uuid.uuid4())
        os.makedirs(f'.files/{folder}', exist_ok=True)

        file_path = f'.files/{folder}/{file.filename}'

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

            # Retornamos error de conflicto (código 409)
            return JSONResponse(content={'error': 'El archivo ya existe'}, status_code=status.HTTP_409_CONFLICT)

        # Registramos el archivo en la base de datos
        new_file = await db["Files"].insert_one({
            "filename": file.filename,
            "folder": folder,
            "path": file_path,
            "hash": hashstring
        })

        # Abrimos el archivo con rasterio
        with rasterio.open(file_path) as dataset:
            # Obtenemos los metadatos
            metadata = {}
            metadata['count'] = dataset.count
            metadata['crs'] = dataset.crs.to_string()
            metadata['dtype'] = dataset.dtypes[0]
            metadata['driver'] = dataset.driver
            metadata['bounds'] = list(dataset.bounds)
            metadata['lnglat'] = list(dataset.lnglat())
            metadata['height'] = dataset.height
            metadata['width'] = dataset.width
            metadata['shape'] = dataset.shape
            metadata['res'] = dataset.res
            metadata['nodata'] = dataset.nodata
            metadata['tags'] = dataset.tags()

            metadata['fileId'] = new_file.inserted_id             

            # Convertimos los metadatos a JSON
            metadata = jsonable_encoder(metadata)

            # Enviamos estos datos al microservicio de metadatos
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8001/', json=metadata) as response:
                    return JSONResponse(content=await response.json(), status_code=status.HTTP_201_CREATED)

    # Si el archivo no es de tipo GeoTiff
    else:
        return JSONResponse(content={'error': 'El archivo no es de tipo GeoTiff'}, status_code=status.HTTP_400_BAD_REQUEST)