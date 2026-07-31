from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.utils import hash_password, verify_password
from app.oauth2 import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: schemas.CreateUser,
    db: Session = Depends(get_db)
):

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return "User registered successfully"


@router.post("/login",response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException( status_code=401,detail="Invalid credentials")

    if not verify_password(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token( data={"user_id": user.id})

    return{
         "access_token": access_token,
         "token_type": "bearer"
    }