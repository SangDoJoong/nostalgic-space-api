"""
콘텐츠 API 라우터 모듈.

이 모듈은 콘텐츠 생성 및 조회와 관련된 엔드포인트를 제공합니다.

작성자:
    kimdonghyeok
"""

from typing import List

from fastapi import APIRouter, Depends

# from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.content import content_service
from api.content.schema.content_schema import ContentCreate, ContentUpdate
from api.user.user_router import get_current_user
from app.api.common.api_response import ApiResponse
from config.database_init import get_db

# from starlette import status


router = APIRouter(prefix="/api/content", tags=["Content"])


@router.post("/", response_model=dict)
def create_content(
    content_create: ContentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    새로운 콘텐츠를 생성합니다.

    Args:
        content_create (ContentCreate): 생성할 콘텐츠의 데이터.
        db (Session): SQLAlchemy 데이터베이스 세션.
        current_user (dict): 현재 로그인된 사용자 정보.

    Returns:
        dict: 생성된 콘텐츠 ID와 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 생성 중 오류가 발생한 경우.
    """
    content = content_service.create_content(current_user, db, content_create)
    return ApiResponse.success(content)


@router.get("/{content_id}", response_model=dict)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """
    콘텐츠의 정보를 조회합니다.
    Args:
        content_id (int): 콘텐츠 ID .
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        dict: 사용자가 생성한 콘텐츠 ID 목록과 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 조회 중 오류가 발생한 경우.
    """
    content = content_service.get_content_detail(db, content_id)
    return ApiResponse.success(content)


@router.get("/user/{username}", response_model=List[int])
def get_user_contents(username: str, db: Session = Depends(get_db)):
    """
    사용자가 작성한 콘텐츠의 정보를 조회합니다.
    Args:
        username (str): 콘텐츠 ID .
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        list: 사용자가 생성한 콘텐츠 ID 목록과 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 조회 중 오류가 발생한 경우.
    """
    contents = content_service.get_user_contents(db, username)
    return ApiResponse.success(contents)


@router.patch("/{content_id}", response_model=dict)
def update_content(
    content_id: int,
    update_data: ContentUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    콘텐츠 일부 필드 수정

    Args:
        content_id (int): 콘텐츠 ID .
        update_data (ContentUpdate): 수정할 콘텐츠 데이터.
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        list: 사용자가 생성한 콘텐츠 ID 목록과 상태 정보를 포함하는 응답.

    Raises:
        HTTPException: 콘텐츠 조회 중 오류가 발생한 경우.
    """
    updated = content_service.update_content(current_user, db, content_id, update_data)
    return ApiResponse.success(updated)


@router.delete("/{content_id}", response_model=dict)
def delete_content(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    콘텐츠 삭제 (Soft delete)

    Args:
        content_id (int): 콘텐츠 ID .
        current_user (dict, optional): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.

    Returns:
        _type_: _description_
    """
    content_service.delete_content(current_user, db, content_id)
    return ApiResponse.success(message="콘텐츠가 삭제되었습니다.")
