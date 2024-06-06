from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from models import Image,UserImage,ContentImage,User
from image import image_crud, image_schema
from image.image_schema import ImageCreate,UserImageCreate,ContentImageCreate
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
        
def create_user_image(db: Session, image_create: ImageCreate, user_id: int):
    try :
        # image db 에 이미지 저장 정보 저장
        db_image= Image( created_at = pendulum.now("Asia/Seoul"),image_address=image_create.image_address)
        db.add(db_image)
        db.flush()
        print("db_Image OK")
        # User 와 Image 를 연결해주는 db 에 값 업데이트
        user_image=UserImage(user_id=user_id,image_id=db_image.image_id)
        db.add(user_image)
        db.flush()
        
        print("image_user OK")
        # User 정보에 저장된 image id  업데이트 
        user = db.query(User).filter(User.uid == user_id).first()
        if user : 
            user.image_id= user_image.id
            db.add(user)
        db.commit()
        
        print("final OK")
        return db_image.image_id
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
def get_user_image(db: Session,user_id: int  ):
    user_image_id= db.query(User).filter(User.uid== user_id).first().image_id
    
    image_id = db.query(UserImage).filter(UserImage.id== user_image_id).first().image_id
    
    image_address = db.query(Image).filter(Image.image_id== image_id).first().image_address
    
    return image_address
def create_content_image(db: Session, image_create: ContentImageCreate):
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
    

