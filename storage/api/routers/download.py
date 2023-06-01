from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse, FileResponse

import aiohttp

import os

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

    # Obtenemos la ruta del archivo desde el microservicio de metadatos
    # (NOTA): Se podría ahorrar esta petición si es que se entregara la ruta direcamente desde el microservicio de almacenamiento al iniciar este endpoint
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://localhost:8001/{id}') as response:
            # Revisar si la respuesta es válida
            if response.status != status.HTTP_200_OK:
                return JSONResponse(content={'error': 'Invalid id'}, status_code=status.HTTP_400_BAD_REQUEST)

            metadata = await response.json()
            file_path = metadata['path']

    # Verificamos que el archivo exista
    if not os.path.isfile(file_path):
        return JSONResponse(content={'error': 'El archivo no existe'}, status_code=status.HTTP_404_NOT_FOUND)

    # Enviamos el archivo al cliente
    return FileResponse(file_path, media_type='image/tiff', status_code=status.HTTP_200_OK)