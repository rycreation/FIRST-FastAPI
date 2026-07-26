from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import (
    get_all_users,
    get_user_by_id,
)
from app.database import get_db
from app.schemas import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me",response_model=UserResponse,)
def read_me(current_user=Depends(get_current_user),):
    return current_user


@router.get("/",response_model=list[UserResponse],)
def read_users(db: Session = Depends(get_db),):
    return get_all_users(db)


@router.get("/{user_id}",response_model=UserResponse,)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id( db, user_id,)

    if not user:
        raise HTTPException( status_code=404,detail="User not found", )

    return user