import pendulum
from content.content_schema import ContentCreate
from fastapi import HTTPException
from models import Content, ContentImage
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def create_content(current_user: dict, db: Session, content_create: ContentCreate):
    try:

        db_content = Content(
            content=content_create.content,
            created_at=pendulum.now("Asia/Seoul"),
            title=content_create.title,
            writer_name=current_user["username"],
            like_cnt=0,
            is_deleted=False,
        )
        db.add(db_content)
        db.flush()
        for image in content_create.image_id:
            db_content_image = ContentImage(
                content_id=db_content.contents_id, image_id=image
            )
            db.add(db_content_image)
        db.commit()

        return db_content.contents_id

    except SQLAlchemyError as e:
        db.rollback()  # 데이터베이스 롤백
        print(f"An error occurred: {e}")  # 오류 메시지 출력 또는 로깅
        raise HTTPException(status_code=500, detail="Internal Server Error")
