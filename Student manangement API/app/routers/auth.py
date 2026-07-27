from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app import models, schemas
from app.utils import hash_password, verify_password
from app.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordBearer
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Register User
@router.post("/register",response_model=schemas.UserResponse)
def register(user:schemas.UserCreate,
             db:Session=Depends(get_db)):

    existing_email=db.query(models.User).filter(models.User.email==user.email).first()

    if existing_email:
        raise HTTPException(status_code=400,detail="Email already registered")

    existing_username=db.query(models.User).filter(models.User.username==user.username).first()

    if existing_username:
        raise HTTPException(status_code=400,detail="Username already exists")

    hashed_password = hash_password(user.password)


    new_user=models.User(username=user.username,
                         email=user.email,
                         password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == form_data.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"user_id": db_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


















#=======THIS CODE DELETE USERS======


# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == user_id).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()

#     return {"message": "User deleted successfully"}