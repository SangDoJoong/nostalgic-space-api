"""
지도 마커 API 라우터

설명:
    이 모듈은 지도 마커와 관련된 API 엔드포인트를 정의합니다.
    지도 마커 정보를 생성하고 조회할 수 있는 기능을 제공합니다.

작성자:
    kimdonghyeok

엔드포인트:
    POST /map_marker/save:
        지도 마커 정보를 생성하여 데이터베이스에 저장합니다.

    GET /maps/{map_point_id}:
        주어진 ID에 해당하는 지도 마커 정보를 조회합니다.

    GET /maps/:
        저장된 모든 지도 마커 목록을 조회합니다.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database_init import get_db

from . import map_crud, map_schema

router = APIRouter()


@router.post("/map_marker/save")
def create_map_point(map_point: map_schema.MapCreate, db: Session = Depends(get_db)):
    """
    지도 마커 정보를 생성하여 데이터베이스에 저장합니다.

    매개변수:
        map_point (map_schema.MapCreate): 생성할 지도 마커의 데이터.
        db (Session): 데이터베이스 세션 객체.

    반환값:
        dict: 상태 코드와 저장 성공 메시지를 포함한 응답.
    """
    map_crud.create_map_point(db=db, map_point=map_point)

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 저장되었습니다.",
        "data": {},
    }


@router.get("/maps/{map_point_id}", response_model=map_schema.MapResponse)
def read_map_point(map_point_id: int, db: Session = Depends(get_db)):
    """
    주어진 ID에 해당하는 지도 마커 정보를 조회합니다.

    매개변수:
        map_point_id (int): 조회할 지도 마커의 ID.
        db (Session): 데이터베이스 세션 객체.

    반환값:
        map_schema.MapResponse: 주어진 ID에 해당하는 지도 마커 정보.

    예외 처리:
        - HTTPException: 지도 마커를 찾을 수 없는 경우 404 오류를 반환합니다.
    """
    db_map_point = map_crud.get_map_point(db, map_point_id=map_point_id)
    if db_map_point is None:
        raise HTTPException(status_code=404, detail="Map point not found")
    return db_map_point


@router.get("/maps/", response_model=list[map_schema.MapResponse])
def read_map_points(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    저장된 모든 지도 마커 목록을 조회합니다.

    매개변수:
        skip (int): 조회를 시작할 항목의 인덱스.
        limit (int): 조회할 항목의 최대 개수.
        db (Session): 데이터베이스 세션 객체.

    반환값:
        list[map_schema.MapResponse]: 저장된 지도 마커 정보 목록.
    """
    map_points = map_crud.get_map_points(db, skip=skip, limit=limit)
    return map_points
