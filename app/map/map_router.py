# map_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import map_crud, map_schema
from database import get_db

router = APIRouter()

@router.post("/map_marker/save")
def create_map_point(map_point: map_schema.MapCreate, db: Session = Depends(get_db)):
    map_crud.create_map_point(db=db, map_point=map_point)
    
    return {
        "status_code": status.HTTP_200_OK,
        "detail":"정상적으로 저장되었습니다.",
        "data":{
        }
    }


# @router.get("/maps/{map_point_id}", response_model=map_schema.MapResponse)
# def read_map_point(map_point_id: int, db: Session = Depends(database.get_db)):
#     db_map_point = map_crud.get_map_point(db, map_point_id=map_point_id)
#     if db_map_point is None:
#         raise HTTPException(status_code=404, detail="Map point not found")
#     return db_map_point

# @router.get("/maps/", response_model=list[map_schema.MapResponse])
# def read_map_points(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
#     map_points = map_crud.get_map_points(db, skip=skip, limit=limit)
#     return map_points