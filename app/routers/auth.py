from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from ..models import User
from ..oauth2 import create_access_token
from ..schemas import Token
from ..utils import verify

router = APIRouter()


@router.post("/login", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # use built-in OAuth2PasswordRequestForm, the user_credential contains following specific fields:
    # username and password

    user = db.query(User).filter(User.email == user_credential.username).first()

    # check the email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # check the password
    if not verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )

    # create a token and return
    access_token = create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
