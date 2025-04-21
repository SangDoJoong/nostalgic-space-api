import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
sqlite_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(sqlite_url, echo=True)


def conn():
    # DB에 연결하여 선언된 테이블들이 존재하는지 확인하고
    # 없다면 테이블들을 생성해준다.
    SQLModel.metadata.create_all(engine)
