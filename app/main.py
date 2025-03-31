from time import sleep
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2 as pypg
from psycopg2.extras import RealDictCursor
from . import models, schema
from sqlalchemy.orm import Session
from .db import engine, get_db
from . import models
import os
from dotenv import load_dotenv

from .routers import post, user, auth

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


# Middleware (use === include_router) method
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Path Operations || Routes
@app.get("/")  # Decorators : Turns the code to path
async def root():  # Function
    return {
        "message": "Hello Monkeys!\nThis is Ritik"
    }  # Message python-dictionary || JSON
