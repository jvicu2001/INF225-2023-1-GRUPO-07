import os

import rasterio

import aiofiles
import aiohttp

import uuid

from fastapi import Body, FastAPI, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type == 'image/tiff':
        # Creamos una carpeta con nombre único
        folder = str(uuid.uuid4())
        os.makedirs(f'.files/{folder}', exist_ok=True)

        file_path = f'.files/{folder}/{file.filename}'

        # Guardamos el archivo en la carpeta
        async with aiofiles.open(file_path, 'wb') as f:
            while content := await file.read(1024):
                await f.write(content)

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
            
            metadata['path'] = file_path
             

            # Convertimos los metadatos a JSON
            metadata = jsonable_encoder(metadata)

            # Enviamos estos datos al microservicio de metadatos
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8001/', json=metadata) as response:
                    return JSONResponse(content=await response.json(), status_code=200)

    # Si el archivo no es de tipo GeoTiff
    else:
        return JSONResponse(content={'error': 'El archivo no es de tipo GeoTiff'}, status_code=400)
