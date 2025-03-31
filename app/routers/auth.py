from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schema, util
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not util.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # Create a token
    return {"token": "example token"}
