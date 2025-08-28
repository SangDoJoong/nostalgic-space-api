"""
이미지 및 관계 데이터 관리 모듈.

이 모듈은 이미지 데이터를 생성하거나 조회하고, 사용자-이미지 및 콘텐츠-이미지 관계를 처리하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

import pendulum
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import app.models.content as content
import app.models.image as image
import app.models.user as user

# ---------------------- #
#   User Profile Image   #
# ---------------------- #


def create_userimage(db: Session, image_path: str, username: str) -> int:
    """
    사용자의 프로필 이미지를 생성하거나 교체

    """
    try:
        user_obj = db.query(user.User).filter(user.User.username == username).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")

        # 새로운 이미지 생성
        db_image = image.Image(
            created_at=pendulum.now("Asia/Seoul"), image_address=image_path
        )
        db.add(db_image)
        db.flush()

        # 기존 이미지 있으면 삭제
        if user_obj.profile_image_id:
            old = (
                db.query(image.Image)
                .filter(image.Image.id == user_obj.profile_image_id)
                .first()
            )
            if old:
                db.delete(old)

        # 유저 프로필 이미지 갱신
        user_obj.profile_image_id = db_image.id
        db.add(user_obj)
        db.commit()
        db.refresh(db_image)
        return db_image.id

    except SQLAlchemyError as e:
        db.rollback()
        print(f"[create_userimage] {e}")
        raise HTTPException(status_code=500, detail="DB Error")


def get_user_image(db: Session, username: str):
    """사용자의 프로필 이미지 조회"""
    user_obj = db.query(user.User).filter(user.User.username == username).first()
    if not user_obj or not user_obj.profile_image_id:
        return None
    return user_obj.profile_image


def delete_user_image(db: Session, username: str) -> bool:
    """사용자의 프로필 이미지 삭제"""
    try:
        user_obj = db.query(user.User).filter(user.User.username == username).first()
        if not user_obj or not user_obj.profile_image_id:
            raise HTTPException(status_code=404, detail="User image not found")

        img = (
            db.query(image.Image)
            .filter(image.Image.id == user_obj.profile_image_id)
            .first()
        )
        if img:
            db.delete(img)
        user_obj.profile_image_id = None
        db.add(user_obj)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[delete_user_image] {e}")
        raise HTTPException(status_code=500, detail="DB Error")


# ---------------------- #
#   Content Images (N:1) #
# ---------------------- #


def create_contentimage(db: Session, image_path: str, content_id: int) -> int:
    """콘텐츠 이미지 생성"""
    try:
        content_obj = (
            db.query(content.Content).filter(content.Content.id == content_id).first()
        )
        if not content_obj:
            raise HTTPException(status_code=404, detail="Content not found")

        db_image = image.Image(
            created_at=pendulum.now("Asia/Seoul"),
            image_address=image_path,
            content_id=content_id,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image.id
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[create_contentimage] {e}")
        raise HTTPException(status_code=500, detail="DB Error")


def get_content_images(db: Session, content_id: int):
    """콘텐츠의 모든 이미지 조회"""
    content_obj = (
        db.query(content.Content).filter(content.Content.id == content_id).first()
    )
    if not content_obj:
        return []
    return content_obj.images


def delete_content_images(db: Session, content_id: int) -> bool:
    """콘텐츠의 모든 이미지 삭제 (개별 삭제 불가)"""
    try:
        imgs = db.query(image.Image).filter(image.Image.content_id == content_id).all()
        if not imgs:
            raise HTTPException(status_code=404, detail="No images found")

        for img in imgs:
            db.delete(img)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[delete_content_images] {e}")
        raise HTTPException(status_code=500, detail="DB Error")
