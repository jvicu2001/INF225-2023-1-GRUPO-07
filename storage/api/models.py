from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import List

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    password_hash: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserInDB(User):
    password_hash: str = Field(...)

class GeoTiffMetadataModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    count: int = Field(...)     # Cantida de bandas
    crs: str = Field(...)       # Coordinate Reference System
    dtype: str = Field(...)     # Tipo de dato (ej: uint8, int16, float32, etc.)
    driver: str = Field(...)    # Driver (ej: GTiff)
    bounds: list = Field(...)   # Bounding Box, en metros (xmin, ymin, xmax, ymax)
    lnglat: List[float] = Field(...)    # Coordenadas de la imagen (longitude, latitude)
    height: int = Field(...)    # Cantidad de filas de la imagen en pixeles
    width: int = Field(...)     # Cantidad de columnas de la imagen en pixeles
    shape: List[int] = Field(...)   # ???
    res: List[float] = Field(...)   # Área de cada pixel (resolución)
    nodata: float = Field(...)
    tags: dict = Field(...)     # Tags
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                    "count": 3,
                    "crs": "EPSG:32618",
                    "dtype": "uint8",
                    "driver": "GTiff",
                    "bounds": [
                        101985.0,
                        2611485.0,
                        339315.0,
                        2826915.0
                    ],
                    "lnglat": [
                        -77.75790625255473,
                        24.561583285327067
                    ],
                    "height": 718,
                    "width": 791,
                    "shape": [
                        718,
                        791
                    ],
                    "res": [
                        300.0379266750948,
                        300.041782729805
                    ],
                    "nodata": 0.0
            }
        }   # Ejemplo de un documento de la colección GeoTiffMetadata
            # Extraido de https://rasterio.readthedocs.io/en/stable/cli.html#info

class FileMetadataModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    fileData: GeoTiffMetadataModel = Field(...)
    user: str = Field(...)
    fileName: str = Field(...)
    fileDataType: int = Field(...)  # 0: DEM, 1: DTM, 2: DSM
    fileId: PyObjectId = Field(...)     # Id del archivo en la colección Files del microservicio storage

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }