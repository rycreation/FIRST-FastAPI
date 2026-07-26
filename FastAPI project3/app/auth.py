from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import ( SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,)
from app.database import get_db
from app.crud import get_user_by_email
from app.schemas import TokenData


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Swagger authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



# Password Functions


def hash_password(password: str) -> str:   #Hash a plain text password
    return pwd_context.hash(password)           


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Verify a plain password against a hashed password
    return pwd_context.verify(plain_password, hashed_password)



# JWT Functions


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
   
   # Create a JWT access token.
   
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY, # type: ignore
        algorithm=ALGORITHM,
    )

    return encoded_jwt


# Current User


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),):
    
    #Return the currently authenticated user.


    credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)

    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM],) # type: ignore

        email: str = payload.get("sub") # type: ignore

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, token_data.email) # type: ignore

    if user is None:
        raise credentials_exception

    return user