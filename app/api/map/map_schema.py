# map_schema.py
from datetime import datetime

from pydantic import BaseModel


class MapCreate(BaseModel):
    content_id: int
    latitude: float
    longitude: float


class MapResponse(BaseModel):
    map_id: int
    content_id: int
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        orm_mode = True
