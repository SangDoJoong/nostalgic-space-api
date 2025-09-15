"""
이미지 업로드 및 조회 API 라우터 모듈.

이 모듈은 사용자 및 콘텐츠와 연결된 이미지를 업로드하고 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok
"""

from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from api.image import image_service
from api.user.user_router import get_current_user
from config.database_init import get_db

router = APIRouter(prefix="/api", tags=["Image"])


# ---------------------- #
#   User Profile Image   #
# ---------------------- #


@router.post("/userimage")
async def upload_userimage(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    img_id = await image_service.create_userimage(db, file, current_user["username"])
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "저장 완료",
        "data": {"image_id": img_id},
    }


@router.get("/userimage")
def get_userimage(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    img = image_service.get_user_image(db, current_user["username"])
    if not img:
        raise HTTPException(404, "프로필 이미지 없음")
    return {"status_code": 200, "data": {"profile_image": img}}


@router.delete("/userimage")
def delete_userimage(
    current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    image_service.delete_user_image(db, current_user["username"])
    return {"status_code": 200, "detail": "프로필 이미지 삭제됨"}


# ---------------------- #
#   Content Images (N:1) #
# ---------------------- #


@router.post("/contentimage")
async def upload_contentimages(
    content_id: int = Query(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...),
):
    ids = await image_service.create_contentimages(db, files, content_id)
    return {"status_code": 200, "detail": "저장 완료", "data": {"image_ids": ids}}


@router.get("/contentimage")
def get_contentimages(content_id: int = Query(...), db: Session = Depends(get_db)):
    imgs = image_service.get_content_images(db, content_id)
    return {"status_code": 200, "data": {"content_images": imgs}}


@router.delete("/contentimage")
def delete_contentimages(content_id: int = Query(...), db: Session = Depends(get_db)):
    image_service.delete_content_images(db, content_id)
    return {"status_code": 200, "detail": "콘텐츠 이미지 전체 삭제됨"}
