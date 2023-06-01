from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from motor import motor_asyncio



import os

router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def search(query=None, page=1, limit=10):
    client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_FILEAPI_URL"])
    db = client.Files

    if query is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder({"error": "No query provided"}))

    files = await db["Files"].find({"filename": {"$regex": query}})\
        .skip((( page - 1 ) * limit) if (page > 0) else 0)\
        .limit(limit)\
        .to_list(limit)
    
    # Devolver código 404 si no se encontraron archivos
    if len(files) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder({"error": "No files found"}))
    
    # Crear una lista de las entradas de la base de datos
    files_data = [jsonable_encoder(file) for file in files]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(files_data))