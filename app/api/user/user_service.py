"""
사용자 관련 데이터 처리 모듈.

이 모듈은 사용자 생성, 조회 및 인증 관련 데이터베이스 작업을 처리합니다.

작성자:
    kimdonghyeok
"""

from datetime import datetime, timedelta

import pendulum
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from api.common.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from api.common.pwd_context import pwd_context
from api.user.schema.login_request_schema import LoginRequestDto
from api.user.schema.user_create_schema import UserCreate
from models.user import User


def create_user(db: Session, user_create: UserCreate):
    """
    새로운 사용자를 생성하고 데이터베이스에 저장합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        user_create (UserCreate): 생성할 사용자 데이터.

    Returns:
        User: 생성된 사용자 객체.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    get_existing_user(db, user_create=user_create)
    db_user = User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        created_at=pendulum.now("Asia/Seoul"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # db_user 객체를 갱신하여 반환
    return db_user


def get_existing_user(db: Session, user_create: UserCreate):
    """
    이미 존재하는 사용자를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        user_create (UserCreate): 조회할 사용자 데이터.

    Returns:
        User or None: 사용자 객체 또는 존재하지 않을 경우 None.
    """
    user = db.query(User).filter(User.username == user_create.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )


def get_user(db: Session, _login_request_dto: LoginRequestDto):
    """
    사용자 이름으로 사용자를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자의 이름.

    Returns:
        User or None: 사용자 객체 또는 존재하지 않을 경우 None.
    """
    user = db.query(User).filter(User.username == _login_request_dto.username).first()
    if not user or not pwd_context.verify(_login_request_dto.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_access_token(user):
    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token
