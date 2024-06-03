from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import Image,UserImage,ContentImage
from image import image_crud, image_schema
from image.image_schema import ImageCreate
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import os
import pendulum
load_dotenv()


def create_image(db: Session, image_create: ImageCreate):
    try :
        db_image= Image( created_at = pendulum.now("Asia/Seoul"),image_address=image_create.image_address)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
def create_user_image(db: Session, image_create: ImageCreate):
    try :
        db_image= Image( created_at = pendulum.now("Asia/Seoul"),image_address=image_create.image_address)
        db.add(db_image)
        db.flush()

        user_image=UserImage(user_id=image_create.user_id,image_id=db_image.image_id)
        db.add(user_image)
        db.commit()
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")

def create_content_image(db: Session, image_create: ImageCreate):
    try :
        db_image= Image( created_at = pendulum.now("Asia/Seoul"),image_address=image_create.image_address)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")