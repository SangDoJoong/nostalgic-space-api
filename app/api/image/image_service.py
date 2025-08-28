"""
이미지 서비스 모듈 (비즈니스 로직).
"""

import os
from datetime import datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from api.image import image_crud


async def save_file(file: UploadFile, upload_dir: str = "/uploads/") -> str:
    """업로드된 파일을 저장하고 경로 반환"""
    try:
        file_contents = await file.read()
        _, ext = os.path.splitext(file.filename)
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{ext}"
        saved_path = os.path.join(upload_dir, filename)
        with open(saved_path, "wb") as f:
            f.write(file_contents)
        return saved_path
    except Exception as e:
        print(f"[save_file] {e}")
        raise HTTPException(status_code=500, detail="File save failed")


# ---------------------- #
#    User Profile Image  #
# ---------------------- #


async def create_userimage(db: Session, file: UploadFile, username: str) -> int:
    """
    사용자의 이미지를 생성하거나 업데이트합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        image_create (ImageCreate): 생성할 이미지의 데이터.
        username (str): 이미지를 연결할 사용자 이름.

    Returns:
        int: 생성 또는 업데이트된 이미지의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    saved_path = await save_file(file)
    return image_crud.create_userimage(db, saved_path, username)


def get_user_image(db: Session, username: str):
    """
    특정 사용자의 이미지 주소를 조회합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 조회할 사용자 이름.

    Returns:
        str: 사용자의 이미지 주소.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    return image_crud.get_user_image(db, username)


def delete_user_image(db: Session, username: str) -> bool:
    """
    특정 사용자의 이미지를 삭제합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        username (str): 삭제할 사용자 이름.

    Returns:
        str: 삭제 성공 여부.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """
    return image_crud.delete_user_image(db, username)


# ---------------------- #
#   Content Images (N:1) #
# ---------------------- #


async def create_contentimages(
    db: Session, files: list[UploadFile], content_id: int
) -> list[int]:
    """
    콘텐츠 이미지를 생성합니다.

    Args:
        db (Session): SQLAlchemy 데이터베이스 세션.
        files (list[UploadFile]): 업로드된 파일 목록.
        content_id (int): 이미지를 연결할 콘텐츠 ID.

    Returns:
        int: 생성된 이미지의 고유 ID.

    Raises:
        HTTPException: 데이터베이스 작업 중 오류가 발생한 경우.
    """

    ids = []
    for f in files:
        saved_path = await save_file(f)
        img_id = image_crud.create_contentimage(db, saved_path, content_id)
        ids.append(img_id)
    return ids


def get_content_images(db: Session, content_id: int):
    return image_crud.get_content_images(db, content_id)


def delete_content_images(db: Session, content_id: int) -> bool:
    return image_crud.delete_content_images(db, content_id)
