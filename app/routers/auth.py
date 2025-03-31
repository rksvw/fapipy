from fastapi import APIRouter, status, HTTPException, Depends
from .. import models, schema, util, oauth2
from sqlalchemy.orm import Session
from ..db import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
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

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # Create a token
    return {"access_token": access_token, "token_type": "bearer"}
