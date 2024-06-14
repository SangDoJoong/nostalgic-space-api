from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from content import content_crud,content_schema
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/api/content",
)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def content_create(_content_create: content_schema.ContentCreate, db: Session = Depends(get_db)):
    print(_content_create)
    content_crud.create_content(db=db,content_create=_content_create)
    
    return {
        "status_code": status.HTTP_200_OK,
        "detail":"정상적으로 생성되었습니다.",
    }
    '''
        user = user_crud.get_existing_user(db, user_create=_user_create)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
            )
        user_crud.create_user(db=db, user_create=_user_create)
    '''

