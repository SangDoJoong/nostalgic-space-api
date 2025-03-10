from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Map, Marker


# 지도 CRUD 함수들
def create_map(db: Session, map_in):
    """
    새로운 지도 레코드를 생성하여 데이터베이스에 저장한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param map_in: 'latitude'와 'longitude' 속성을 포함하는 입력 객체.
    :return: 생성된 Map 인스턴스.
    """
    point = f"POINT({map_in.longitude} {map_in.latitude})"
    db_map = Map(center_location=func.ST_GeomFromText(point, 4326))
    db.add(db_map)
    db.commit()
    db.refresh(db_map)
    return db_map


def get_map(db: Session, map_id: int):
    """
    지정된 ID를 가진 지도 레코드를 조회한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param map_id: 조회할 지도 ID.
    :return: 조회된 Map 인스턴스 또는 존재하지 않을 경우 None.
    """
    return db.query(Map).filter(Map.map_id == map_id).first()


def update_map(db: Session, map_id: int, map_in):
    """
    지정된 ID의 지도 레코드를 업데이트한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param map_id: 업데이트할 지도 ID.
    :param map_in: 업데이트할 'latitude'와 'longitude' 값을 포함하는 입력 객체.
    :return: 업데이트된 Map 인스턴스 또는 해당 레코드가 없을 경우 None.
    """
    db_map = get_map(db, map_id)
    if not db_map:
        return None
    point = f"POINT({map_in.longitude} {map_in.latitude})"
    db_map.center_location = func.ST_GeomFromText(point, 4326)
    db.commit()
    db.refresh(db_map)
    return db_map


def delete_map(db: Session, map_id: int):
    """
    지정된 ID의 지도 레코드를 삭제한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param map_id: 삭제할 지도 ID.
    :return: 삭제된 Map 인스턴스 또는 해당 레코드가 없을 경우 None.
    """
    db_map = get_map(db, map_id)
    if not db_map:
        return None
    db.delete(db_map)
    db.commit()
    return db_map


# 마커 CRUD 함수들
def create_marker(db: Session, marker_in):
    """
    새로운 마커 레코드를 생성하여 데이터베이스에 저장한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param marker_in: 'map_id', 'latitude', 'longitude', 'uid', 'content_id' 등의 속성을 포함하는 입력 객체.
    :return: 생성된 Marker 인스턴스.
    """
    point = f"POINT({marker_in.longitude} {marker_in.latitude})"
    db_marker = Marker(
        map_id=marker_in.map_id,
        latitude=marker_in.latitude,
        longitude=marker_in.longitude,
        location=func.ST_GeomFromText(point, 4326),
        uid=marker_in.uid,
        content_id=marker_in.content_id,
    )
    db.add(db_marker)
    db.commit()
    db.refresh(db_marker)
    return db_marker


def get_marker(db: Session, marker_id: int):
    """
    지정된 ID를 가진 마커 레코드를 조회한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param marker_id: 조회할 마커 ID.
    :return: 조회된 Marker 인스턴스 또는 존재하지 않을 경우 None.
    """
    return db.query(Marker).filter(Marker.marker_id == marker_id).first()


def update_marker(db: Session, marker_id: int, marker_in):
    """
    지정된 ID의 마커 레코드를 업데이트한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param marker_id: 업데이트할 마커 ID.
    :param marker_in: 업데이트할 'map_id', 'latitude', 'longitude', 'uid', 'content_id' 등의 속성을 포함하는 입력 객체.
    :return: 업데이트된 Marker 인스턴스 또는 해당 레코드가 없을 경우 None.
    """
    db_marker = get_marker(db, marker_id)
    if not db_marker:
        return None
    point = f"POINT({marker_in.longitude} {marker_in.latitude})"
    db_marker.map_id = marker_in.map_id
    db_marker.latitude = marker_in.latitude
    db_marker.longitude = marker_in.longitude
    db_marker.location = func.ST_GeomFromText(point, 4326)
    db_marker.uid = marker_in.uid
    db_marker.content_id = marker_in.content_id
    db.commit()
    db.refresh(db_marker)
    return db_marker


def delete_marker(db: Session, marker_id: int):
    """
    지정된 ID의 마커 레코드를 삭제한다.

    :param db: SQLAlchemy Session 인스턴스.
    :param marker_id: 삭제할 마커 ID.
    :return: 삭제된 Marker 인스턴스 또는 해당 레코드가 없을 경우 None.
    """
    db_marker = get_marker(db, marker_id)
    if not db_marker:
        return None
    db.delete(db_marker)
    db.commit()
    return db_marker
