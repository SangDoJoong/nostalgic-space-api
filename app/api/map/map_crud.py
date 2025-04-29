"""
지도 마커 데이터베이스 작업 모듈

설명:
    이 모듈은 지도 마커와 관련된 데이터베이스 작업을 수행하는 함수를 정의합니다.
    데이터베이스에 새 지도 마커를 생성하고, 저장된 마커 정보를 조회하는 기능을 제공합니다.

작성자:
    kimdonghyeok

함수:
    create_map_point(db: Session, map_point: map_schema.MapResponse):
        새로운 지도 마커를 생성하여 데이터베이스에 저장하고, 생성된 마커 객체를 반환합니다.

    get_map_point(db: Session, map_point_id: int):
        주어진 ID에 해당하는 지도 마커 정보를 반환합니다.

    get_map_points(db: Session, skip: int, limit: int):
        저장된 지도 마커 목록을 조회하여 반환합니다.
"""

from sqlalchemy.orm import Session

from models import map_marker

from . import map_schema


def create_map_point(db: Session, map_point: map_schema.MapResponse):
    """
    새로운 지도 마커를 생성하여 데이터베이스에 저장하고, 생성된 마커 객체를 반환합니다.

    매개변수:
        db (Session): 데이터베이스 세션 객체.
        map_point (map_schema.MapResponse): 생성할 지도 마커의 데이터.

    반환값:
        map_marker: 생성된 지도 마커 객체.
    """
    db_map_point = map_marker(
        latitude=map_point.latitude,
        longitude=map_point.longitude,
        location=f"POINT({map_point.longitude} {map_point.latitude})",
    )
    db.add(db_map_point)
    db.commit()
    db.refresh(db_map_point)
    return db_map_point


def get_map_point(db: Session, map_point_id: int):
    """
    주어진 ID에 해당하는 지도 마커 정보를 반환합니다.

    매개변수:
        db (Session): 데이터베이스 세션 객체.
        map_point_id (int): 조회할 지도 마커의 ID.

    반환값:
        map_marker: 주어진 ID에 해당하는 지도 마커 객체.
    """
    return db.query(map_marker).filter(map_marker.map_id == map_point_id).first()


def get_map_points(db: Session, skip: int = 0, limit: int = 100):
    """
    저장된 지도 마커 목록을 조회하여 반환합니다.

    매개변수:
        db (Session): 데이터베이스 세션 객체.
        skip (int): 조회를 시작할 항목의 인덱스.
        limit (int): 조회할 항목의 최대 개수.

    반환값:
        List[map_marker]: 저장된 지도 마커 객체 목록.
    """
    return db.query(map_marker).offset(skip).limit(limit).all()
