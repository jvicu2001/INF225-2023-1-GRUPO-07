from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import uvicorn

from routers import download, upload, search, auth

app = FastAPI()

app.include_router(download.router)
app.include_router(upload.router)
app.include_router(search.router)
app.include_router(auth.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@app.get("/")
async def root(token: str = Depends(oauth2_scheme)):
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8020, host="0.0.0.0", log_level="info", reload=True)