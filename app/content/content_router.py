from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException,File,UploadFile,Form
from fastapi import Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database.database_init import get_db
from content import content_crud
from user.user_router import get_current_user
from image.image_router import save_file
from image.image_schema import ImageCreate
from content.content_schema import ContentCreate
import os


router = APIRouter(
    prefix="/api/content",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

@router.post("/create")
async def content_create( content_create: ContentCreate
    , db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    try:
        _content_create=ContentCreate(title=content_create.title,content=content_create.content)
        contents_id=content_crud.create_content(current_user,db=db,content_create=_content_create)

    
        return {
            "status_code": status.HTTP_200_OK,
            "detail": "정상적으로 저장되었습니다.",
            "data":{ 
                "content_id_index " : contents_id
                }
        }
    except HTTPException as e:
            raise e
    
'''
@router.get("/refresh", status_code=status.HTTP_204_NO_CONTENT)
def content_refresh( db: Session = Depends(get_db)):
    
    #content_crud.create_content(db=db,content_create=_content_create)
    
    return {
        "status_code": status.HTTP_200_OK,
        "detail":"정상적으로 생성되었습니다.",
    }
'''
