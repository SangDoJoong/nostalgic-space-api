from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


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
