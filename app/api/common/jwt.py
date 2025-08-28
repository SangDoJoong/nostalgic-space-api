from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette import status

from config.settings import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# Bearer 인증 스키마 (Swagger에서는 단순 토큰 입력창으로 나옴)
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    현재 사용자 확인 (Bearer 토큰 인증)
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = {"username": username}
    except JWTError:
        raise credentials_exception
    else:
        return token_data
