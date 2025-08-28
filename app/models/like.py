from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Like(SQLModel, table=True):
    __tablename__ = "likes"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    target_id: int
    target_type: str = Field(..., max_length=20)
    created_at: datetime = Field(..., nullable=False)
