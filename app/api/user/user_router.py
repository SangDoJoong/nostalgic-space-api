"""
사용자 인증 및 관리 API 라우터 모듈.

이 모듈은 사용자 생성, 로그인, 토큰 발급, 사용자 정보 조회 등 인증 및 관리 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from api.common.api_response import ApiResponse
from api.common.jwt import get_current_user
from api.user import user_service
from api.user.schema.login_request_schema import LoginRequestDto
from api.user.schema.user_create_schema import UserCreate
from config.database_init import get_db

router = APIRouter(
    prefix="/api/user",
)


@router.post("/create", status_code=status.HTTP_200_OK)
def user_create(_user_create: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자를 생성합니다.

    Args:
        _user_create (UserCreate): 생성할 사용자 데이터.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 생성 성공 메시지와 상태 코드.

    Raises:
        HTTPException: 사용자가 이미 존재할 경우 409 상태 코드 반환.
    """
    user_service.create_user(db=db, user_create=_user_create)

    return ApiResponse.ok()


@router.post("/login")
def login_for_access_token(
    _login_request_dto: LoginRequestDto, db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 액세스 토큰 발급.

    Args:
        form_data (OAuth2PasswordRequestForm): 사용자 로그인 데이터 (username, password).
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 액세스 토큰 및 사용자 정보.

    Raises:
        HTTPException: 인증 실패 시 401 상태 코드 반환.
    """
    print("----접근~~")
    user = user_service.get_user(db, _login_request_dto)
    access_token = user_service.get_access_token(user)

    return ApiResponse.success(access_token)


@router.post("/token")
def login_for_access_token_with_token(
    _login_request_dto: LoginRequestDto, db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 액세스 토큰 발급 (중복 함수).

    Args:
        form_data (OAuth2PasswordRequestForm): 사용자 로그인 데이터 (username, password).
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 액세스 토큰 정보.

    Raises:
        HTTPException: 인증 실패 시 401 상태 코드 반환.
    """
    user = user_service.get_user(db, _login_request_dto)
    access_token = user_service.get_access_token(user)

    return ApiResponse.success(access_token)


@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    """
    현재 로그인된 사용자의 정보를 반환합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.

    Returns:
        dict: 현재 사용자의 정보.
    """
    return ApiResponse.success(current_user)
