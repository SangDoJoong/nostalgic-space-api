# map_crud.py
from datetime import datetime

from sqlalchemy.orm import Session

from models import Content, Map

from .map_schema import MapCreate


def create_map_marker(db: Session, map_data: MapCreate):
    content = (
        db.query(Content).filter(Content.contents_id == map_data.content_id).first()
    )
    if not content:
        return None
    db_map = Map(
        content_id=map_data.content_id,
        latitude=map_data.latitude,
        longitude=map_data.longitude,
        created_at=datetime.utcnow(),
    )
    db.add(db_map)
    try:
        db.commit()
    except Exception as e:
        print(e)
    db.refresh(db_map)

    return db_map


def get_map_marker(db: Session, map_id: int):
    return db.query(Map).filter(Map.map_id == map_id).first()


def get_marker_by_content(db: Session, content_id: int):
    return db.query(Map).filter(Map.content_id == content_id).first()
