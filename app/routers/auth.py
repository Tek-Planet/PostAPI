
from app.routers import oauth2
from ..database import get_db
from .. import models, schemas, util
from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(tags=["Authenticaation"])


@router.post("/login")
def login(user_credential:
          #  schemas.UserLogin use this to send the data in json foe manner
          OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")

    if not util.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token}
