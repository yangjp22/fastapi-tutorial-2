import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import db_config


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        params = db_config.config("app/database.ini")
        conn = psycopg2.connect(
            **params,
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

app = FastAPI()


my_posts = [
    {'title': 'The first one', 'content': 'The first content', 'id': 1},
    {'title': 'The second one', 'content': 'The second content', 'id': 2}
]


@app.get('/')
async def root():
    return {'message': 'Hello world'}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return {'posts': posts}


@app.get("/posts/{idx}")
def get_post(idx: int):
    cursor.execute("select * from posts where id = {}".format(idx))
    post = cursor.fetchone()
    if post:
        return {'post': post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='post with id: {} was not found.'.format(idx)
    )

# def get_post(idx: int, response: Response):
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'msg': 'post with id: {} was not found.'.format(idx)}


@app.post("/posts", status_code=status.HTTP_200_OK)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (
            post_dict['title'],
            post_dict['content']))
    new_post = cursor.fetchone()
    conn.commit()  # 需要执行提交的对象是connection

    return {'post': new_post}


def find_index_post(idx):
    for i, post in enumerate(my_posts):
        if post['id'] == idx:
            return i
    return -1


@app.delete('/posts/{idx}')
def delete_post(idx: int):
    cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(idx), ))
    delete_post = cursor.fetchone()
    conn.commit()

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="post with id: {} was not found.".format(idx)
        )

    return {'post': delete_post}


@app.put("/posts/{idx}")
def update_post(idx: int, post: Post):
    cursor.execute("UPDATE posts set title=%s, content=%s where id=%s returning *""", (post.title, post.content, str(idx)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='post with id: {} was not found.'.format(idx)
        )

    return {'post': updated_post}
