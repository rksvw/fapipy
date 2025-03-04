from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


# Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# data
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like Spaghetti", "id": 2},
    {"title": "title of post 1", "content": "content of post 1", "id": 3},
    {"title": "title of post 1", "content": "content of post 1", "id": 4},
    {"title": "title of post 1", "content": "content of post 1", "id": 5},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_n_delete(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


# Path Operations || Routes
@app.get("/")  # Decorators : Turns the code to path
async def root():  # Function
    return {
        "message": "Hello Monkeys!\nThis is Ritik"
    }  # Message python-dictionary || JSON


@app.get("/post")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(
    post: Post,
):  # Extract all the value from body and make python dictionary
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)

    return {
        "data": my_posts,
    }


@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"data": post}


# title: str, content: str


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    idx = find_n_delete(id)

    if idx == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists.",
        )

    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
