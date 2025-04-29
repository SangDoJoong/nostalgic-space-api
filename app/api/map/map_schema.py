"""
지도 마커 데이터 모델

설명:
    이 모듈은 지도 마커와 관련된 요청 및 응답 데이터 모델을 정의합니다.
    FastAPI와 Pydantic을 사용하여 요청 데이터의 유효성을 검사하고 구조를 정의합니다.

작성자:
    kimdonghyeok

클래스:
    MapCreate:
        지도 마커 생성 요청 데이터를 검증하는 모델.

    MapResponse:
        지도 마커 조회 응답 데이터를 검증하는 모델.
"""

from pydantic import BaseModel


class MapCreate(BaseModel):
    """
    지도 마커 생성 요청 데이터를 검증하는 모델.

    속성:
        latitude (float): 마커의 위도.
        longitude (float): 마커의 경도.
        uid (int): 사용자 ID.
        content_id (int): 콘텐츠 ID.
    """

    latitude: float
    longitude: float
    uid: int
    content_id: int


class MapResponse(BaseModel):
    """
    지도 마커 조회 응답 데이터를 검증하는 모델.

    속성:
        map_id (int): 마커 ID.
        latitude (float): 마커의 위도.
        longitude (float): 마커의 경도.
    """

    map_id: int
    latitude: float
    longitude: float
