from datetime import datetime

from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    __tablename__ = "Images"

    image_id: int | None = Field(default=None, primary_key=True)
    image_address: str = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)
