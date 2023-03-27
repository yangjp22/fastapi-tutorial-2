from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
