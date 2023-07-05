from datetime import datetime, timedelta

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from motor import motor_asyncio

from jose import JWTError, jwt

import os

from models import User, Token, TokenData, UserInDB

SECRET_KEY = open("/run/secrets/oauth-secret", "r").read()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# Token generation
@router.post("/token", response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    client = motor_asyncio.AsyncIOMotorClient(f'{os.environ["MONGODB_URL"]}')
    db = client.Users

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"error": "Incorrect username or password"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Register user
@router.post("/register", response_model=User)
async def register(username: str, password: str):
    client = motor_asyncio.AsyncIOMotorClient(f'{os.environ["MONGODB_URL"]}')
    db = client.Users
    if await db["Users"].find_one({"username": username}) is not None:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "Username already exists"})
    password_hash = get_password_hash(password)
    user = UserInDB(username=username, password_hash=password_hash)
    await db["Users"].insert_one(user.dict(by_alias=True))
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db: motor_asyncio.AsyncIOMotorClient, username: str) -> UserInDB | None:
    user: dict | None = await db["Users"].find_one({"username": username})
    if user is not None:
        return UserInDB(**user)
    
async def authenticate_user(db: motor_asyncio.AsyncIOMotorClient, username: str, password: str) -> User | None:
    user = await get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt