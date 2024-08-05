from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User
from user.user_schema import UserCreate
import pendulum


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        username=user_create.username, password=pwd_context.hash(user_create.password1), created_at = pendulum.now("Asia/Seoul")
    )
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter((User.username == user_create.username)).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
