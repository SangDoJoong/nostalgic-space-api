"""
Pydantic 스키마 정의 모듈.

이 모듈은 콘텐츠 생성/수정 요청 및 응답과 관련된 Pydantic 스키마를 정의합니다.

작성자:
    kimdonghyeok
"""

from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel, ValidationInfo, field_validator
from starlette import status


class BaseOrmModel(BaseModel):
    model_config = {"from_attributes": True}  # pydantic v2 ORM 지원 설정


# ----------------------
# 콘텐츠 생성/수정 요청
# ----------------------


class ContentCreate(BaseOrmModel):
    """
    콘텐츠 생성 요청 데이터 모델.
    """

    title: str
    content: str
    map_id: int
    image_ids: Optional[List[int]] = []  # 여러 장 이미지 업로드 지원

    @field_validator("title", "content")
    @classmethod
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.name}은(는) 비어있을 수 없습니다.",
            )
        return v


class ContentUpdate(BaseOrmModel):
    """
    콘텐츠 수정 요청 데이터 모델.
    """

    title: Optional[str] = None
    content: Optional[str] = None
    image_ids: Optional[List[int]] = None  # 전체 교체

    @field_validator("title", "content")
    @classmethod
    def not_empty_if_provided(cls, v: Optional[str], info: ValidationInfo):
        if v is not None and not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{info.field_name}은(는) 공백일 수 없습니다.",
            )
        return v


# ----------------------
# 콘텐츠 응답
# ----------------------


class ContentResponse(BaseOrmModel):
    """
    콘텐츠 응답 데이터 모델.
    """

    id: int
    title: Optional[str]
    content: Optional[str]
    writer_name: Optional[str]
    created_at: datetime
    like_cnt: int
    is_deleted: bool
    map_id: Optional[int]
    image_ids: List[int] = []


# ----------------------
# 인증 토큰
# ----------------------


class Token(BaseOrmModel):
    """
    인증 토큰 데이터 모델.
    """

    access_token: str
    token_type: str
