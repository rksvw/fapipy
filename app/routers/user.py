from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schema, util
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):

    # Has the password - user.password
    hash_password = util.hash_me(user.password)
    user.password = hash_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Inside get route seperated commas(,) parameters called decorator
@router.get("/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with id: {id} does not exist",
        )

    return user
