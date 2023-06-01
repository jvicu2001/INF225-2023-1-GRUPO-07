import os
from fastapi import Body, FastAPI, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from bson import ObjectId

import pymongo

from typing import List

from .models import GeoTiffMetadataModel

import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.Metadata

@app.post("/metadata/", response_model=GeoTiffMetadataModel, response_model_exclude_unset=True, response_description="Add metadata from GeoTiff file")
async def add_metadata(metadata: GeoTiffMetadataModel = Body(...)):
    metadata = jsonable_encoder(metadata)
    new_metadata = await db["GeoTiffMetadata"].insert_one(metadata)
    created_metadata = await db["GeoTiffMetadata"].find_one({"_id": new_metadata.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_metadata)

@app.get("/metadata/", response_description="Get list of metadata from GeoTiff files", response_model=List[GeoTiffMetadataModel])
async def get_metadata(page: int = 0, limit: int = 25):
    metadata = await db["GeoTiffMetadata"].find()\
        .sort("_id", pymongo.ASCENDING)\
        .skip((( page - 1 ) * limit) if (page > 0) else 0)\
        .limit(limit)\
        .to_list(limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content=metadata)

@app.get("/metadata/{id}", response_description="Get metadata from GeoTiff file", response_model=GeoTiffMetadataModel)
async def get_metadata_by_id(id: str):
    if (metadata := await db["GeoTiffMetadata"].find_one({"_id": id})) is not None:
        return metadata

    raise HTTPException(status_code=404, detail=f"Metadata {id} not found")
