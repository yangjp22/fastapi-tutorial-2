from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

from app.schemas import PostUpdate, PostResponse, PostCreate
from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import UserResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db),
              user_id: UserResponse = Depends(get_current_user)):
    # cursor.execute("select * from posts")
    # posts = cursor.fetchall()

    # sqlalchemy way
    posts = db.query(models.Post).all()
    return posts


@router.get("/{idx}", response_model=PostResponse)
def get_post(idx: int, db: Session = Depends(get_db),
             user_id: UserResponse = Depends(get_current_user)):
    # cursor.execute("select * from posts where id = {}".format(idx))
    # post = cursor.fetchone()

    # sqlalchemy way
    post = db.query(models.Post).filter(models.Post.id == idx).first()
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='post with id: {} was not found.'.format(idx)
    )


@router.post("/", status_code=status.HTTP_200_OK, response_model=PostResponse)
def create_posts(
        new_post: PostCreate,
        db: Session = Depends(get_db),
        user_id: UserResponse = Depends(get_current_user)):  # we can use user_id in this function now
    print(user_id)
    print(user_id.password)
    # post_dict = new_post.dict()
    # cursor.execute(
    #     """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (
    #         post_dict['title'],
    #         post_dict['content']))
    # new_post = cursor.fetchone()
    # conn.commit()  # 需要执行提交的对象是connection

    # sqlalchemy way
    # added_post = models.Post(**new_post.dict())
    added_post = models.Post(
        title=new_post.title,
        content=new_post.content,
        published=new_post.published)  # 创建一条数据记录
    db.add(added_post)  # 将记录加到数据表中
    db.commit()  # 提交
    db.refresh(added_post)  # 刷新

    return added_post


@router.delete('/{idx}')
def delete_post(idx: int, db: Session = Depends(get_db),
                user_id: UserResponse = Depends(get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts where id = %s returning *""", (str(idx), ))
    # delete_post = cursor.fetchone()
    # conn.commit()

    # sqlalchemy way
    deleted_post = db.query(models.Post).filter(models.Post.id == idx)

    if not deleted_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post with id: {} was not found.".format(idx)
        )

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return deleted_post


@router.put("/{idx}", response_model=PostResponse)
def update_post(
        idx: int,
        post: PostUpdate,
        db: Session = Depends(get_db),
        user_id: UserResponse = Depends(get_current_user)):
    # cursor.execute(
    #     "UPDATE posts set title=%s, content=%s where id=%s returning *"
    #     "", (post.title, post.content, str(idx)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # sqlalchemy way
    updated_query = db.query(models.Post).filter(models.Post.id == idx)
    if not updated_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='post with id: {} was not found.'.format(idx)
        )
    updated_query.update(post.dict(),
                         synchronize_session=False)
    db.commit()
    return updated_query.first()
