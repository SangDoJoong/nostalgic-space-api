from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import Image
from image import image_crud, image_schema
from image.image_schema import ImageCreate
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import os
import pendulum
load_dotenv()



def create_image(db: Session, image_create: ImageCreate, _image_url):
    try :
        db_image= Image(
            user_id = image_create.user_id,content_id= image_create.content_id , created_at = pendulum.now("Asia/Seoul"),image_address=_image_url
        )
        print(db_image)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
