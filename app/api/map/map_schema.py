from typing import Optional

from pydantic import BaseModel


# 지도 관련 스키마
class MapBase(BaseModel):
    """
    지도 기본 스키마.

    지도에 대한 기본 위치 정보를 담고 있으며, 위도와 경도 값을 포함한다.

    :ivar latitude: 지도 중심의 위도.
    :ivar longitude: 지도 중심의 경도.
    """

    latitude: float
    longitude: float


class MapCreate(MapBase):
    """
    지도 생성 스키마.

    지도 생성 시 필요한 입력 데이터를 정의한다.
    추가 필드가 필요한 경우 확장하여 사용할 수 있다.
    """

    pass


class MapResponse(MapBase):
    """
    지도 응답 스키마.

    생성된 지도 정보를 클라이언트에 응답하기 위한 스키마로,
    지도 고유 식별자인 map_id를 포함한다.

    :ivar map_id: 생성된 지도 레코드의 고유 식별자.
    """

    map_id: int

    class Config:
        orm_mode = True


# 마커 관련 스키마
class MarkerBase(BaseModel):
    """
    마커 기본 스키마.

    지도 상의 개별 마커에 대한 위치 및 관련 정보를 포함한다.

    :ivar map_id: 해당 마커가 속한 지도의 ID.
    :ivar latitude: 마커의 위도.
    :ivar longitude: 마커의 경도.
    :ivar uid: 마커와 관련된 사용자 ID (옵션).
    :ivar content_id: 마커와 관련된 콘텐츠 ID (옵션).
    """

    map_id: int
    latitude: float
    longitude: float
    uid: Optional[int] = None
    content_id: Optional[int] = None


class MarkerCreate(MarkerBase):
    """
    마커 생성 스키마.

    새로운 마커를 생성할 때 필요한 데이터를 정의한다.
    MarkerBase를 상속받아 기본 필드를 포함한다.
    """

    pass


class MarkerResponse(MarkerBase):
    """
    마커 응답 스키마.

    생성된 마커 정보를 클라이언트에 응답하기 위한 스키마로,
    마커 고유 식별자인 marker_id를 추가로 포함한다.

    :ivar marker_id: 생성된 마커 레코드의 고유 식별자.
    """

    marker_id: int

    class Config:
        orm_mode = True
