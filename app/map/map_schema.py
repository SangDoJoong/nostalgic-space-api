from pydantic import BaseModel

class MapCreate(BaseModel):
    latitude: float
    longitude: float
    uid: int
    content_id: int

class MapResponse(BaseModel):
    map_id: int
    latitude: float
    longitude: float
    uid: int
    content_id: int
