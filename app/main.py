from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import db_config
from . import models
from .database import engine, get_db
from .routers import user, post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])

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


@app.get('/')
async def root():
    return {'message': 'Hello world'}
