from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.image import Image


class Content(SQLModel, table=True):
    __tablename__ = "contents"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None, nullable=True)
    content: Optional[str] = Field(default=None, nullable=True)
    writer_name: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(..., nullable=False)
    like_cnt: int = Field(default=0, nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    map_id: Optional[int] = Field(default=None, foreign_key="maps.id")

    images: List["Image"] = Relationship(back_populates="content")
    comments: List["Comment"] = Relationship(back_populates="post")
