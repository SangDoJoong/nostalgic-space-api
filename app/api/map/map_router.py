from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database_init import get_db

from . import map_crud, map_schema

router = APIRouter()

# 지도 관련 라우터


@router.post("/maps", response_model=map_schema.MapResponse)
def create_map(map_in: map_schema.MapCreate, db: Session = Depends(get_db)):
    """
    새 지도를 생성하는 엔드포인트.

    :param map_in: 생성할 지도 정보를 담은 MapCreate 스키마 객체. (예: 위도, 경도 등)
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 생성된 지도 정보를 담은 MapResponse 스키마 객체.
    """
    db_map = map_crud.create_map(db, map_in)
    return map_schema.MapResponse(
        map_id=db_map.map_id, latitude=map_in.latitude, longitude=map_in.longitude
    )


@router.get("/maps/{map_id}", response_model=map_schema.MapResponse)
def read_map(map_id: int, db: Session = Depends(get_db)):
    """
    지정한 ID의 지도를 조회하는 엔드포인트.

    :param map_id: 조회할 지도 ID.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 조회된 지도 정보를 담은 MapResponse 스키마 객체.
    :raises HTTPException: 지도 정보가 없을 경우 404 에러 발생.
    """
    db_map = map_crud.get_map(db, map_id)
    if not db_map:
        raise HTTPException(status_code=404, detail="Map not found")
    # center_location에서 위도/경도를 추출하는 처리는 상황에 맞게 구현 필요
    return map_schema.MapResponse(map_id=db_map.map_id, latitude=0.0, longitude=0.0)


@router.put("/maps/{map_id}", response_model=map_schema.MapResponse)
def update_map(
    map_id: int, map_in: map_schema.MapCreate, db: Session = Depends(get_db)
):
    """
    지정한 ID의 지도 정보를 업데이트하는 엔드포인트.

    :param map_id: 업데이트할 지도 ID.
    :param map_in: 업데이트할 지도 정보를 담은 MapCreate 스키마 객체.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 업데이트된 지도 정보를 담은 MapResponse 스키마 객체.
    :raises HTTPException: 업데이트할 지도 정보가 없을 경우 404 에러 발생.
    """
    db_map = map_crud.update_map(db, map_id, map_in)
    if not db_map:
        raise HTTPException(status_code=404, detail="Map not found")
    return map_schema.MapResponse(
        map_id=db_map.map_id, latitude=map_in.latitude, longitude=map_in.longitude
    )


@router.delete("/maps/{map_id}")
def delete_map(map_id: int, db: Session = Depends(get_db)):
    """
    지정한 ID의 지도를 삭제하는 엔드포인트.

    :param map_id: 삭제할 지도 ID.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 삭제 결과를 나타내는 메시지.
    :raises HTTPException: 삭제할 지도 정보가 없을 경우 404 에러 발생.
    """
    db_map = map_crud.delete_map(db, map_id)
    if not db_map:
        raise HTTPException(status_code=404, detail="Map not found")
    return {"detail": "Map deleted"}


# 마커 관련 라우터


@router.post("/markers", response_model=map_schema.MarkerResponse)
def create_marker(marker_in: map_schema.MarkerCreate, db: Session = Depends(get_db)):
    """
    새 마커를 생성하는 엔드포인트.

    :param marker_in: 생성할 마커 정보를 담은 MarkerCreate 스키마 객체.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 생성된 마커 정보를 담은 MarkerResponse 스키마 객체.
    """
    db_marker = map_crud.create_marker(db, marker_in)
    return map_schema.MarkerResponse(
        marker_id=db_marker.marker_id,
        map_id=db_marker.map_id,
        latitude=marker_in.latitude,
        longitude=marker_in.longitude,
        uid=db_marker.uid,
        content_id=db_marker.content_id,
    )


@router.get("/markers/{marker_id}", response_model=map_schema.MarkerResponse)
def read_marker(marker_id: int, db: Session = Depends(get_db)):
    """
    지정한 ID의 마커를 조회하는 엔드포인트.

    :param marker_id: 조회할 마커 ID.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 조회된 마커 정보를 담은 MarkerResponse 스키마 객체.
    :raises HTTPException: 조회할 마커 정보가 없을 경우 404 에러 발생.
    """
    db_marker = map_crud.get_marker(db, marker_id)
    if not db_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return map_schema.MarkerResponse(
        marker_id=db_marker.marker_id,
        map_id=db_marker.map_id,
        latitude=db_marker.latitude,
        longitude=db_marker.longitude,
        uid=db_marker.uid,
        content_id=db_marker.content_id,
    )


@router.put("/markers/{marker_id}", response_model=map_schema.MarkerResponse)
def update_marker(
    marker_id: int, marker_in: map_schema.MarkerCreate, db: Session = Depends(get_db)
):
    """
    지정한 ID의 마커 정보를 업데이트하는 엔드포인트.

    :param marker_id: 업데이트할 마커 ID.
    :param marker_in: 업데이트할 마커 정보를 담은 MarkerCreate 스키마 객체.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 업데이트된 마커 정보를 담은 MarkerResponse 스키마 객체.
    :raises HTTPException: 업데이트할 마커 정보가 없을 경우 404 에러 발생.
    """
    db_marker = map_crud.update_marker(db, marker_id, marker_in)
    if not db_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return map_schema.MarkerResponse(
        marker_id=db_marker.marker_id,
        map_id=db_marker.map_id,
        latitude=marker_in.latitude,
        longitude=marker_in.longitude,
        uid=db_marker.uid,
        content_id=db_marker.content_id,
    )


@router.delete("/markers/{marker_id}")
def delete_marker(marker_id: int, db: Session = Depends(get_db)):
    """
    지정한 ID의 마커를 삭제하는 엔드포인트.

    :param marker_id: 삭제할 마커 ID.
    :param db: 데이터베이스 세션 (SQLAlchemy Session).
    :return: 삭제 결과를 나타내는 메시지.
    :raises HTTPException: 삭제할 마커 정보가 없을 경우 404 에러 발생.
    """
    db_marker = map_crud.delete_marker(db, marker_id)
    if not db_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return {"detail": "Marker deleted"}
