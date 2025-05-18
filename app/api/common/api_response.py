from typing import Generic, Optional, TypeVar

from fastapi import status
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    status_code: int = status.HTTP_200_OK
    detail: str = "요청이 정상적으로 처리되었습니다."
    data: Optional[T] = None

    @classmethod
    def ok(cls) -> "ApiResponse[None]":
        return cls(status_code=status.HTTP_200_OK, detail="OK", data=None)

    @classmethod
    def success(cls, data: T) -> "ApiResponse[T]":
        return cls(status_code=status.HTTP_200_OK, detail="OK", data=data)
