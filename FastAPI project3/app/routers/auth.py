from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import ( create_access_token,
    hash_password,
    verify_password,
)
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud import ( create_user,get_user_by_email,)
from app.database import get_db
from app.schemas import (
    Token,UserCreate,
    UserResponse,
)

router = APIRouter(tags=["Authentication"])


@router.post( "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
def register( user: UserCreate,db: Session = Depends(get_db),):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered",)

    hashed_password = hash_password(user.password)

    return create_user(
        db=db,
        user=user,
        hashed_password=hashed_password,
    )


@router.post("/login",response_model=Token,)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException( status_code=401,detail="Invalid email or password",)

    if not verify_password( form_data.password, user.password,): # type: ignore
        raise HTTPException( status_code=401, detail="Invalid email or password",)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta( minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }