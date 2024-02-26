from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User
from user.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        name=user_create.name, password=pwd_context.hash(user_create.password1)
    )
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter((User.name == user_create.name)).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.name == username).first()
