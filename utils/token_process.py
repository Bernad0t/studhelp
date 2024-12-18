from datetime import datetime, timedelta

from fastapi import HTTPException

from config import EXPIRE_ACCESS_TOKEN, SECRET_KEY_TOKEN, ALGORITHM
from jose import jwt, exceptions


def create_access_token(data: dict):# лучше по id будет искать чем по токену. так быстрее
    to_encode = data.copy()

    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_ACCESS_TOKEN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, ALGORITHM)

    # return the generated token
    return encoded_jwt

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY_TOKEN, ALGORITHM)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="X-Token header invalid")
    except:
        raise HTTPException(status_code=409, detail="X-Token header invalid")