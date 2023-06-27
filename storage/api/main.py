from fastapi import FastAPI
import uvicorn

from routers import download, upload, search

app = FastAPI()

app.include_router(download.router)
app.include_router(upload.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8020, host="0.0.0.0", log_level="info", reload=True)