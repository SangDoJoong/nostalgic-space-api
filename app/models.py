"""
데이터베이스 모델 정의 모듈.

이 모듈은 데이터베이스에 저장될 사용자, 이미지, 사용자-이미지 관계, 콘텐츠-이미지 관계와 관련된 모델을 정의합니다.

작성자:
    kimdonghyeok
"""

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from config.database_init import Base


class User(Base):
    """
    사용자 모델.

    데이터베이스에 저장될 사용자 정보를 나타냅니다.

    Attributes:
        uid (int): 사용자 고유 식별자.
        password (str): 사용자 비밀번호.
        created_at (datetime): 사용자 계정 생성일.
        username (str): 사용자 이름.
    """

    __tablename__ = "Users"

    uid = Column(Integer, primary_key=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    username = Column(String, nullable=False)


class Content(Base):
    """
    콘텐츠 모델.

    데이터베이스에 저장될 콘텐츠 정보를 나타냅니다.

    Attributes:
        contents_id (int): 콘텐츠 고유 식별자.
        title (str): 콘텐츠 제목.
        content (str): 콘텐츠 내용.
        writer_name (str): 작성자 이름.
        created_at (datetime): 콘텐츠 생성일.
        like_cnt (int): 콘텐츠 좋아요 수.
        is_deleted (bool): 콘텐츠 삭제 여부.
    """

    __tablename__ = "Contents"

    contents_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    writer_name = Column(String, primary_key=False)
    created_at = Column(DateTime, nullable=False)
    like_cnt = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False)


class Image(Base):
    """
    이미지 모델.

    데이터베이스에 저장될 이미지 정보를 나타냅니다.

    Attributes:
        image_id (int): 이미지 고유 식별자.
        image_address (str): 이미지 파일 경로 또는 URL.
        created_at (datetime): 이미지 생성일.
    """

    __tablename__ = "Images"

    image_id = Column(Integer, primary_key=True)
    image_address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)


class UserImage(Base):
    """
    사용자-이미지 관계 모델.

    사용자가 업로드한 이미지와의 관계를 나타냅니다.

    Attributes:
        id (int): 고유 식별자.
        user_id (int): 사용자 ID.
        image_id (int): 이미지 ID.
    """

    __tablename__ = "Users_Images"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=False)
    image_id = Column(Integer, primary_key=False)


class ContentImage(Base):
    """
    콘텐츠-이미지 관계 모델.

    콘텐츠와 첨부된 이미지 간의 관계를 나타냅니다.

    Attributes:
        id (int): 고유 식별자.
        content_id (int): 콘텐츠 ID.
        image_id (int): 이미지 ID.
    """

    __tablename__ = "Contents_Images"
    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, primary_key=False)
    image_id = Column(Integer, primary_key=False)


class Map(Base):
    """
    지도 정보를 저장하는 모델 클래스.

    이 클래스는 지도 중심 좌표 정보를 PostGIS의 POINT 타입으로 관리합니다.

    :ivar map_id: 지도 고유 식별자 (자동 증가, 기본키).
    :ivar center_location: 지도 중심 좌표를 저장하는 컬럼. PostGIS의 POINT 타입을 사용.
    """

    __tablename__ = "maps"
    map_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 지도 중심 좌표 (PostGIS 사용)
    center_location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)


class Marker(Base):
    """
    지도에 표시되는 마커 정보를 저장하는 모델 클래스.

    이 클래스는 각 마커의 위치 정보와 추가 메타데이터(사용자 ID, 콘텐츠 ID 등)를 관리합니다.
    마커는 특정 지도에 소속되며, 지도와의 외래키 관계를 유지합니다.

    :ivar marker_id: 마커 고유 식별자 (자동 증가, 기본키).
    :ivar map_id: 마커가 속한 지도 ID. 'maps' 테이블의 외래키.
    :ivar latitude: 마커의 위도 값.
    :ivar longitude: 마커의 경도 값.
    :ivar location: 마커 위치 정보를 저장하는 컬럼. PostGIS의 POINT 타입을 사용.
    :ivar uid: 마커와 관련된 사용자 ID (옵션).
    :ivar content_id: 마커와 관련된 콘텐츠 ID (옵션).
    """

    __tablename__ = "markers"
    marker_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    map_id = Column(
        Integer, ForeignKey("maps.map_id", ondelete="CASCADE"), nullable=False
    )
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    # 마커 위치 (PostGIS geometry)
    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)
    uid = Column(Integer, nullable=True)
    content_id = Column(Integer, nullable=True)
