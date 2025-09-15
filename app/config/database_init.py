from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config.settings import settings

DB_HOST = settings.DB_HOST
DB_NAME = settings.DB_NAME
DB_USERNAME = settings.DB_USERNAME
DB_PASSWORD = settings.DB_PASSWORD

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def conn():
    try:
        """
        데이터베이스 연결을 초기화하고, 필요한 테이블을 생성합니다.
        """
        # if not SQLModel.metadata.tables:
        #    import app.models.comment
        #    import app.models.content
        #    import app.models.image
        #    import app.models.like
        #    import app.models.map
        #    import app.models.user

        print("Registered tables:")
        for table_name in SQLModel.metadata.tables:
            print("-", table_name)
        SQLModel.metadata.create_all(engine)

    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise
