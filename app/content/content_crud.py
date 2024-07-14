from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import Content,ContentImage
from fastapi import APIRouter, HTTPException
from typing import List
from content.content_schema import ContentCreate
import pendulum
from sqlalchemy.exc import SQLAlchemyError

def create_content(current_user: dict,db: Session, content_create: ContentCreate, image_ids: List[int]):
    try:

        db_content = Content(
            content = content_create.content,
            created_at = pendulum.now("Asia/Seoul"),
            title = content_create.title,
            writer_name =current_user["username"],
            like_cnt = 0,
            is_deleted= False,
        )
        db.add(db_content)
        db.flush()

        for _image_id in image_ids:
            db_content_image = ContentImage(
            content_id=db_content.contents_id,
            image_id=_image_id
            )
            db.add(db_content_image)
        
        db.commit()

        return db_content.contents_id
        
        
    
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
