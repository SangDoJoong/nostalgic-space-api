from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "Users"

    uid: int | None = Field(default=None, primary_key=True)
    password: str = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)
    username: str = Field(..., nullable=False)
