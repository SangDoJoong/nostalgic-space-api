# map_schema.py
from datetime import datetime

from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    class Config:
        from_attributes = True


class MapCreate(BaseOrmModel):
    content_id: int
    latitude: float
    longitude: float


class MapResponse(BaseOrmModel):
    map_id: int
    latitude: float
    longitude: float
    created_at: datetime
