from datetime import datetime

from sqlmodel import Field, SQLModel


class Map(SQLModel, table=True):
    __tablename__ = "maps"

    map_id: int | None = Field(default=None, primary_key=True)
    latitude: float = Field(..., nullable=False)
    longitude: float = Field(..., nullable=False)
    created_at: datetime = Field(..., nullable=False)
