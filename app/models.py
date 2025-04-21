"""
데이터베이스 모델 정의 모듈.

이 모듈은 데이터베이스에 저장될 사용자, 이미지, 사용자-이미지 관계, 콘텐츠-이미지 관계와 관련된 모델을 정의합니다.

작성자:
    kimdonghyeok
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "Users"

    uid: int | None = Field(default=None, primary_key=True)
    password: str = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)
    username: str = Field(..., nullable=False)


class Content(SQLModel, table=True):
    __tablename__ = "Contents"

    contents_id: int | None = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None, nullable=True)
    content: Optional[str] = Field(default=None, nullable=True)
    writer_name: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(..., nullable=False)
    like_cnt: int = Field(..., nullable=False)
    is_deleted: bool = Field(..., nullable=False)
    map_id: Optional[int] = Field(default=None, foreign_key="maps.map_id")


class Image(SQLModel, table=True):
    __tablename__ = "Images"

    image_id: int | None = Field(default=None, primary_key=True)
    image_address: str = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)


class UserImage(SQLModel, table=True):
    __tablename__ = "Users_Images"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(..., nullable=False)
    image_id: int = Field(..., nullable=False)


class ContentImage(SQLModel, table=True):
    __tablename__ = "Contents_Images"

    id: int | None = Field(default=None, primary_key=True)
    content_id: int = Field(..., nullable=False)
    image_id: int = Field(..., nullable=False)


class Map(SQLModel, table=True):
    __tablename__ = "maps"

    map_id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., nullable=False)
    longitude: float = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)
