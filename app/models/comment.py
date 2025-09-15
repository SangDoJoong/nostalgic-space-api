from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.content import Content


class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    content_id: int = Field(foreign_key="contents.id")
    text: str
    created_at: datetime = Field(..., nullable=False)

    post: Optional["Content"] = Relationship(back_populates="comments")

    parent_id: Optional[int] = Field(default=None, foreign_key="comments.id")
    parent: Optional["Comment"] = Relationship(
        back_populates="replies", sa_relationship_kwargs={"remote_side": "Comment.id"}
    )
    replies: List["Comment"] = Relationship(back_populates="parent")
