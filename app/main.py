from time import sleep
import os
from dotenv import load_dotenv, dotenv_values
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 as pypg
from psycopg2.extras import RealDictCursor

app = FastAPI()

load_dotenv()

PASS = os.getenv("PASSWORD")


# Schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = pypg.connect(
            host="localhost",
            database="fastApi",
            user="postgres",
            password=PASS,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"Erro: {error}")
        sleep(2)


# Here I learn how to use FastAPI and some CRUD operation [get, post & delete]
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


def find_idx(id):
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
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"message": "Post retrive Successfully", "data": posts}


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
    idx = find_idx(id)

    if idx == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists.",
        )
        # SELECT * FROM products WHERE name LIKE '%en%';
        # SELECT * FROM products WHERE price > 10 LIMIT 5;
        # SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;

    my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    idx = find_idx(id)

    if idx == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    post_dict = post.dict()
    post_dict["id"] = id  # Here we are creating new id post data
    my_posts[idx] = post_dict  # Here we are storing the user generated data into post
    return {"data": post_dict}  # Return the data
