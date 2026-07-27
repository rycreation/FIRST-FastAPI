from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

#create a JWT token
def create_access_token(data:dict):  
    to_encode=data.copy()
    expire= datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) # type: ignore

    return encode_jwt


def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) # type: ignore
        return payload
    except JWTError:
        return None