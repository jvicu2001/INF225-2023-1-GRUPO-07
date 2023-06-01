from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse, FileResponse

import motor.motor_asyncio

from bson import ObjectId

import os

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_FILEAPI_URL"])

router = APIRouter(
    prefix="/download",
    tags=["download"],
    responses={404: {"description": "Not found"}},
)

@router.get("/") # id obtenido desde el microservicio de metadatos
async def download_file(id: str):
    # Devolver código 400 si no se entregó un id
    if id is None:
        return JSONResponse(content={'error': 'No id provided'}, status_code=status.HTTP_400_BAD_REQUEST)

    # Buscamos el archivo en la base de datos
    db = client.Files
    file = await db["Files"].find_one({"_id": ObjectId(id)})

    # Verificamos que el archivo exista
    if file is None:
        return JSONResponse(content={'error': 'El archivo no existe'}, status_code=status.HTTP_404_NOT_FOUND)

    if not os.path.isfile(file['path']):
        return JSONResponse(content={'error': 'El archivo está registrado pero no existe. Contactar administrador'}, status_code=status.HTTP_404_NOT_FOUND)

    # Enviamos el archivo al cliente
    return FileResponse(file['path'], media_type='image/tiff', status_code=status.HTTP_200_OK)