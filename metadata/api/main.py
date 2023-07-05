import os
from fastapi import Body, FastAPI, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from bson import ObjectId

from sys import argv

import pymongo

import uvicorn

from typing import List

from models import FileMetadataModel

import motor.motor_asyncio

from routes import auth

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(f'{os.environ["MONGODB_URL"]}')
db = client.Metadata

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

app.include_router(auth.router)

@app.post("/metadata/", response_model=FileMetadataModel, response_model_exclude_unset=True, response_description="Add metadata from GeoTiff file")
async def add_metadata(metadata: FileMetadataModel = Body(...), token : str = Depends(oauth2_scheme)):    
    metadata = jsonable_encoder(metadata)
    new_metadata = await db["Metadata"].insert_one(metadata)
    created_metadata = await db["Metadata"].find_one({"_id": new_metadata.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_metadata)

@app.get("/metadata/", response_description="Get list of metadata from GeoTiff files", response_model=List[FileMetadataModel])
async def get_metadata(query: str | None = None, page: int = 0, limit: int = 25):
    if query:
        metadata = await db["Metadata"].find({"fileName": query})\
            .skip((( page - 1 ) * limit) if (page > 0) else 0)\
            .limit(limit)\
            .to_list(limit)
    else:
        metadata = await db["Metadata"].find()\
            .skip((( page - 1 ) * limit) if (page > 0) else 0)\
            .limit(limit)\
            .to_list(limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content=metadata)

@app.get("/metadata/{id}/", response_description="Get metadata from GeoTiff file", response_model=FileMetadataModel)
async def get_metadata_by_id(id: str):
    if (metadata := await db["Metadata"].find_one({"_id": id})) is not None:
        return metadata

    raise HTTPException(status_code=404, detail=f"Metadata {id} not found")

# Dev environment flag
isDev: bool = False
if len(argv) > 1:
    if (argv[1] == "1"):
        isDev = True

if __name__ == "__main__":
    uvicorn.run("main:app", port=8010, host="0.0.0.0", log_level="info", reload=isDev)