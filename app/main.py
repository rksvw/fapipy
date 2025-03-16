from time import sleep
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2 as pypg
from typing import Optional, List
from psycopg2.extras import RealDictCursor
from . import models, schema
from sqlalchemy.orm import Session
from .db import engine, get_db
from . import models
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

PASS = os.getenv("PASSWORD")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(
    post: schema.PostCreate, db: Session = Depends(get_db)
):  # Extract all the value from body and make python dictionary
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    # More easier way to input the client data into server
    # new_post = models.Post(
    # title=post.title, content=post.content, published=post.published
    # )

    # Convert the post schema to json
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return post


# title: str, content: str


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists.",
        )
        # SELECT * FROM products WHERE name LIKE '%en%';
        # SELECT * FROM products WHERE price > 10 LIMIT 5;
        # SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;
    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schema.Post)
def update_post(id: int, up_post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    # """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    # (post.title, post.content, post.published, (str(id))),
    # )
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = updated_post.first()

    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    updated_post.update(up_post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()  # Return the data
