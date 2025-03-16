from pydantic import BaseModel
from datetime import datetime


# Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    create_at: datetime

    class Config:
        orm_mode = True
