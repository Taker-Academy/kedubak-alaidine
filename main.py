import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from typing import Optional

from datetime import datetime

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="kedubak API",
    summary="API for kedubak project",
)

PyObjectId = Annotated[str, BeforeValidator(str)]

mongo_host = os.environ["MONGO_HOST"]
mongo_port = os.environ["MONGO_PORT"]
mongo_name = os.environ["MONGO_NAME"]

client = AsyncIOMotorClient(f"mongodb://{mongo_host}:{mongo_port}")
db = client.get_database(mongo_name)
users_collection = db.get_collection("users")
posts_collection = db.get_collection("posts")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await users_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        return user
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    email: str
    first_name: str
    last_name: str
    password: str
    last_upvote: datetime = Field(default_factory=datetime.utcnow)
    id: Optional[PyObjectId] = Field(alias="_id", default=None)


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class CommentsModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    first_name: str
    content: str


class UpdatePostModel(BaseModel):
    content: Optional[str] = None


class Post(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    first_name: str
    title: str
    content: str
    comments: List[CommentsModel]
    upvotes: List[str]


class UpdatePostModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.post("auth/register")
async def register(body):
    new_user = await users_collection.insert_one(body)
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return created_user


@app.post("auth/login")
async def login(body):
    user = await users_collection.find_one({"email": body["email"]})
    if user["password"] == body["password"]:
        return user
    return {"message": "Invalid credentials"}


@app.get("/user/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.put("/edit")
async def edit_user(body, current_user: dict = Depends(get_current_user)):
    user = await users_collection.find_one_and_update(
        {"email": body["email"]},
        {
            "firstName": body["firstName"],
            "lastName": body["lastName"],
            "password": body["password"],
        },
        {"password": body["password"]},
        {"lastName": body["lastName"]},
        {"$set": body.dict(exclude_unset=True)},
        return_document=ReturnDocument.AFTER,
    )
    return user


@app.delete("/remove")
async def remove_user(body, current_user: dict = Depends(get_current_user)):
    user = await users_collection.delete_one({"email": body["email"]})
    return user


@app.get("/post/")
async def get_posts(current_user: dict = Depends(get_current_user)):
    posts = await posts_collection.find().to_list(1000)
    return posts


@app.post("/post/")
async def create_post(body, current_user: dict = Depends(get_current_user)):
    new_post = await posts_collection.insert_one(body)
    created_post = await posts_collection.find_one({"_id": new_post.inserted_id})
    return created_post


@app.get("/me")
async def get_me(body, current_user: dict = Depends(get_current_user)):
    user = await users_collection.find_one({"email": body["email"]})
    return user


@app.get("/:{id}")
async def get_post(id, current_user: dict = Depends(get_current_user)):
    post = await posts_collection.find_one({"_id": id})
    return post


@app.delete("/:{id}")
async def delete_post(id, current_user: dict = Depends(get_current_user)):
    post = await posts_collection.delete_one({"_id": id})
    return post


@app.post("/vote/:{id}")
async def upvote_post(id, body, current_user: dict = Depends(get_current_user)):
    post = await posts_collection.find_one({"_id": id})
    if body["email"] in post["upvotes"]:
        return {"message": "User already upvoted"}
    post = await posts_collection.find_one_and_update(
        {"_id": id},
        {"$push": {"upvotes": body["email"]}},
        return_document=ReturnDocument.AFTER,
    )
    return post


@app.post("/comment/:{id}")
async def comment_post(id, body, current_user: dict = Depends(get_current_user)):
    post = await posts_collection.find_one({"_id": id})
    new_comment = CommentsModel(
        user_id=body["user_id"], first_name=body["first_name"], content=body["content"]
    )
