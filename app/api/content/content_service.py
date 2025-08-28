"""
콘텐츠 생성 및 조회 관련 함수 모듈.

이 모듈은 데이터베이스에서 콘텐츠를 생성하거나 특정 사용자와 관련된 콘텐츠를 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

from fastapi import HTTPException

# from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.api.content.content_crud as crud
from api.content.schema.content_schema import ContentCreate, ContentUpdate

# from app.models.content import Content
# from app.models.image import Image
# from app.models.user import User


def create_content(current_user: dict, db: Session, content_create: ContentCreate):
    """
    새로운 콘텐츠를 데이터베이스에 생성합니다.
    """
    return crud.create_content(db, content_create, current_user["username"])


def get_content_detail(db: Session, content_id: int):
    """
    특정 사용자가 작성한 콘텐츠의 정보를 조회합니다.
    """
    content = crud.get_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    return content


def get_user_contents(db: Session, username: str):
    """
    특정 사용자가 작성한 콘텐츠 ID 목록을 조회합니다.
    """
    return crud.get_user_contents(db, username)


def update_content(
    current_user: dict, db: Session, content_id: int, update_data: ContentUpdate
):
    """
    콘텐츠 일부 필드 수정

    Args:
        current_user (dict): _description_
        db (Session): _description_
        content_id (int): _description_
        update_data (ContentUpdate): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    content = crud.get_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠를 찾을 수 없습니다.")
    if content.writer_name != current_user["username"]:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    return crud.update_content(db, content_id, update_data)


def delete_content(current_user: dict, db: Session, content_id: int):
    """
    콘텐츠 삭제 (Soft delete)

    """
    content = crud.get_content(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="콘텐츠가 존재하지 않습니다.")
    if content.writer_name != current_user["username"]:
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    return crud.delete_content(db, content_id)
