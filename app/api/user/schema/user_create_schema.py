from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from starlette import status


class UserCreate(BaseModel):
    """
    사용자 생성 요청 데이터 모델.

    Attributes:
        username (str): 사용자 이름.
        password1 (str): 사용자 비밀번호.
        password2 (str): 비밀번호 확인용 필드.

    Validators:
        not_empty: `username`, `password1`, `password2` 필드가 비어있지 않은지 검증.
        passwords_match: `password1`과 `password2`가 일치하는지 검증.
    """

    username: str
    password1: str
    password2: str

    @field_validator("username", "password1", "password2")
    @classmethod
    def not_empty(cls, v):
        """
        필드 값이 비어 있지 않은지 검증합니다.

        Args:
            v (str): 검증할 값.

        Returns:
            str: 유효한 값.

        Raises:
            HTTPException: 값이 비어있거나 공백인 경우 400 상태 코드 반환.
        """
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="빈 값은 허용되지 않습니다.",
            )
        return v

    @field_validator("password2")
    @classmethod
    def passwords_match(cls, v, info: ValidationInfo):
        """
        `password1`과 `password2`가 일치하는지 확인합니다.

        Args:
            v (str): 검증할 값 (`password2`).
            values (dict): 모델의 다른 필드 값.

        Returns:
            str: 유효한 값.

        Raises:
            HTTPException: 두 비밀번호가 일치하지 않을 경우 400 상태 코드 반환.
        """
        if "password1" in info.data and v != info.data["password1"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="비밀번호가 일치하지 않습니다",
            )
        return v
