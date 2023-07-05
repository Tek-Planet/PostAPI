

from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    name: str
    password: str


class CreateUser(User):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):

    email: EmailStr
    password: str
