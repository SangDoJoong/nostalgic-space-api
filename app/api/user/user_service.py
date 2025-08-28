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

# import app.models.content as content  # Content 모델 (사용자가 작성한 콘텐츠 등 참조 가능)
# import app.models.image as image  # Image 모델 (profile_image 참조용)
import app.models.user as user  # User 모델
from api.common.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from api.common.pwd_context import pwd_context
from api.user.schema.login_request_schema import LoginRequestDto
from api.user.schema.user_create_schema import UserCreate


# ---------------------- #
#      사용자 생성        #
# ---------------------- #
def create_user(db: Session, user_create: UserCreate) -> user.User:
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

    db_user = user.User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        created_at=pendulum.now("Asia/Seoul"),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
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
    existing = (
        db.query(user.User).filter(user.User.username == user_create.username).first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 존재하는 사용자입니다.",
        )


# ---------------------- #
#   사용자 조회 / 로그인   #
# ---------------------- #
def get_user(db: Session, _login_request_dto: LoginRequestDto) -> user.User:
    """
    로그인 요청 DTO로 사용자 조회 및 비밀번호 검증.
    """
    db_user = (
        db.query(user.User)
        .filter(user.User.username == _login_request_dto.username)
        .first()
    )
    if not db_user or not pwd_context.verify(
        _login_request_dto.password, db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user


# ---------------------- #
#    JWT 액세스 토큰 발급   #
# ---------------------- #
def get_access_token(db_user: user.User) -> str:
    """
    주어진 사용자로부터 JWT 액세스 토큰을 생성합니다.
    """
    data = {
        "sub": db_user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
