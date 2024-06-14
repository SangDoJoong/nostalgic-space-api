from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import Content
from fastapi import APIRouter, HTTPException
from content.content_schema import ContentCreate
import pendulum
from sqlalchemy.exc import SQLAlchemyError

def create_content(db: Session, content_create: ContentCreate):
    try:
        db_content = Content(
            content=content_create.content,
            writer_id = content_create.writer_id,
            created_at = pendulum.now("Asia/Seoul")
            
        )
        db.add(db_content)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
