# map_crud.py
from sqlalchemy.orm import Session
from . import map_schema
from models import Map

def create_map_point(db: Session, map_point: map_schema.MapResponse):
    db_map_point = Map(
        latitude=map_point.latitude,
        longitude=map_point.longitude,
        location=f'POINT({map_point.longitude} {map_point.latitude})',
    )
    db.add(db_map_point)
    db.commit()
    db.refresh(db_map_point)
    return db_map_point

# def get_map_point(db: Session, map_point_id: int):
#     return db.query(models.Map).filter(models.Map.map_id == map_point_id).first()

# def get_map_points(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Map).offset(skip).limit(limit).all()
