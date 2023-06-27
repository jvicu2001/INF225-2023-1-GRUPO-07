from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from motor import motor_asyncio

from bson import json_util
import json

import os

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def search(query: str | None = None, page: int = 1, limit: int = 10):
    client = motor_asyncio.AsyncIOMotorClient(f'{os.environ["MONGODB_URL"]}')
    db = client.Files

    files: list = []

    if query is None:
        files = await db["Files"].find()\
            .skip((( page - 1 ) * limit) if (page > 0) else 0)\
            .limit(limit)\
            .to_list(limit)

    else:
        files = await db["Files"].find({"filename": {"$regex": query}})\
            .skip((( page - 1 ) * limit) if (page > 0) else 0)\
            .limit(limit)\
            .to_list(limit)
    
    # Devolver código 404 si no se encontraron archivos
    if len(files) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"error": "No files found"}))
    
    # Crear una lista de las entradas de la base de datos
    files_data = [json.loads(json_util.dumps(file)) for file in files]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(files_data))