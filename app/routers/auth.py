from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..oauth2 import create_access_token
from ..schemas import UserLogin
from ..utils import verify

router = APIRouter()


@router.post("/login")
def login(user_credential: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credential.email).first()

    # check the email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    # check the password
    if not verify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    # create a token and return
    access_token = create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
