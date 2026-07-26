from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User


def get_database() -> Session:
   
   # Database dependency.
   
    return Depends(get_db)


def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    """
    Returns the authenticated user.
    You can add checks here later (e.g., is_active).
    """
    return current_user