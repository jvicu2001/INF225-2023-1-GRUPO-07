from fastapi import FastAPI

from .routers import download, upload, search

app = FastAPI()

app.include_router(download.router)
app.include_router(upload.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}