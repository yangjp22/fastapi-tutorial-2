from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time

from . import db_config

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:604030@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # 负责和数据库建立连接connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # 所有表的建立的基础类


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
