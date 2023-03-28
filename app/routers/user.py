from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.schemas import UserResponse, UserCreate
from .. import models
from ..database import get_db
from ..utils import hashed

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{idx}", response_model=UserResponse)
def get_user(idx: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == idx)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with id: {} was not found.".format(idx)
        )

    return user.first()


@router.post("/",
             status_code=status.HTTP_200_OK,
             response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existed = db.query(
        models.User).filter(
        models.User.email == user.email).first()
    if existed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email: {} exists.".format(user.email)
        )

    # hash the password
    user.password = hashed(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
