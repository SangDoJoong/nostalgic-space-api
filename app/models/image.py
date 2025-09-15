from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.content import Content
    from app.models.user import User


class Image(SQLModel, table=True):
    __tablename__ = "images"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    image_address: str = Field(..., nullable=False)
    sort_order: Optional[int] = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # FK → contents.id (이미지 ↔ 콘텐츠, N:1)
    content_id: Optional[int] = Field(default=None, foreign_key="contents.id")
    content: Optional["Content"] = Relationship(back_populates="images")

    # ✅ User 프로필 이미지에서 참조됨 (역참조)
    user: Optional["User"] = Relationship(back_populates="profile_image")
