"""
콘텐츠 생성 및 조회 관련 함수 모듈 (CRUD 레이어).

데이터베이스에서 콘텐츠를 생성하거나 특정 사용자와 관련된 콘텐츠를 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.models.content as content
from api.content.schema.content_schema import ContentCreate, ContentUpdate


def create_content(
    db: Session, content_create: ContentCreate, username: str
) -> content.Content:
    """
    새로운 콘텐츠를 데이터베이스에 생성합니다.

    Args:
        current_user (dict): 현재 로그인된 사용자 정보.
        db (Session): SQLAlchemy 데이터베이스 세션.
        content_create (ContentCreate): 생성할 콘텐츠의 데이터.

    Returns:
        int: 생성된 콘텐츠의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """

    try:
        db_content = content.Content(
            title=content_create.title,
            content=content_create.content,
            writer_name=username,
            created_at=datetime.now(timezone.utc),  # ✅ 생성 시점 자동 추가
            like_cnt=0,
            is_deleted=False,
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")


def get_content(db: Session, content_id: int) -> content.Content:
    """
    콘텐츠 ID를 기반으로 정보를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        content_id (int): 조회할 사용자의 이름.

    Returns:
        content.Content: 사용자가 작성한 콘텐츠 정보.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.

    """
    return (
        db.query(content.Content)
        .filter(content.Content.id == content_id, content.Content.is_deleted is False)
        .first()
    )


def get_user_contents(db: Session, username: str):
    """
    특정 사용자가 작성한 콘텐츠 ID 목록을 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자의 이름.

    Returns:
        list: 사용자가 작성한 콘텐츠 ID의 목록.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """
    try:
        contents_list = [
            content.id
            for content in db.query(content.Content)
            .filter(
                content.Content.writer_name == username,
                content.Content.is_deleted is False,
            )
            .all()
        ]
        print(contents_list)
        return contents_list
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")


def update_content(
    db: Session, content_id: int, update_data: ContentUpdate
) -> content.Content:
    """
    특정 사용자가 작성한 콘텐츠 ID 목록을 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자의 이름.

    Returns:
        list: 사용자가 작성한 콘텐츠 ID의 목록.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """
    try:
        db_content = (
            db.query(content.Content)
            .filter(
                content.Content.id == content_id, content.Content.is_deleted is False
            )
            .first()
        )
        if not db_content:
            return None

        if update_data.title is not None:
            db_content.title = update_data.title
        if update_data.content is not None:
            db_content.content = update_data.content

        db.commit()
        db.refresh(db_content)
        return db_content
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")


def delete_content(db: Session, content_id: int) -> bool:
    """
    콘텐츠 id를 기반으로 논리 삭제 처리합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        content_id (int): 조회할 사용자의 이름.

    Returns:
        bool: 삭제 성공 여부.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우 500 상태 코드 반환.
    """
    try:
        db_content = (
            db.query(content.Content).filter(content.Content.id == content_id).first()
        )
        if not db_content:
            return False
        db_content.is_deleted = True
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")
