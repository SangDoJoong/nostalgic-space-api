from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database.database_init import get_db
from models import Image,UserImage,ContentImage,User
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
        
def create_user_image(db: Session, image_create: ImageCreate, username: str):
    try :
        user_id=db.query(User).filter(User.username == username).first().uid
        # 사용자가 기존에 이미지를 가지고 있는지 확인
        existing_user_image = db.query(UserImage).filter(UserImage.user_id == user_id).first()
        # image db 에 이미지 저장 정보 저장
        db_image= Image( created_at = pendulum.now("Asia/Seoul"),image_address=image_create.image_address)
        db.add(db_image)
        db.flush()
        if existing_user_image:
            # 사용자가 기존 이미지를 가지고 있다면 해당 이미지 정보를 업데이트
            existing_user_image.image_id = db_image.image_id
            db.add(existing_user_image)
        else:
            # 사용자가 기존 이미지를 가지고 있지 않다면 새로운 UserImage 관계를 추가
            user_image = UserImage(user_id=user_id, image_id=db_image.image_id)
            db.add(user_image)
        db.commit()
        
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def get_user_image(db: Session,username:str ):
    try:
        user_image_id= db.query(User).filter(User.username== username).first().uid

        image_id = db.query(UserImage).filter(UserImage.user_id== user_image_id).first().image_id

        image_address = db.query(Image).filter(Image.image_id== image_id).first().image_address

        return image_address
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")

