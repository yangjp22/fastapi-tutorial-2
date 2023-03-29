from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas
from .database import get_db
from .models import User
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')

# Secret_key
# Algorithm
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Token三要素: header, payload, secret
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# API can verify the token from the browser
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        idx: str = payload.get("user_id")
        if not idx:
            raise credentials_exception
        token_data = schemas.TokenData(id=idx)
        return token_data
    except JWTError as e:
        print(e)
        raise credentials_exception


# 会作为一个Depends项，根据headers中带的token自动解析出user_id
def get_current_user(
        token: str = Depends(oauth2_schema),
        db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(User).filter(User.id == str(token_data.id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")
    return user
