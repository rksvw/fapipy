from fastapi import APIRouter, Response, status, HTTPException, Depends
from .. import models, schema
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
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


@router.get("/{id}", response_model=schema.Post)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schema.Post)
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
