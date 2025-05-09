from pydantic import BaseModel


class Token(BaseModel):
    """
    인증 토큰 데이터 모델.

    Attributes:
        access_token (str): 인증에 사용되는 액세스 토큰.
        token_type (str): 토큰 유형 (예: Bearer).
        username (str): 토큰이 발급된 사용자의 이름.
    """

    access_token: str
    token_type: str
    username: str
