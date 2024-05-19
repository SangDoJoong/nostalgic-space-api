from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends,File ,UploadFile,Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from database import get_db
from image import image_crud, image_schema
from image.image_schema import ImageCreate
from dotenv import load_dotenv
import os

load_dotenv()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
router = APIRouter(
    prefix="/api/image",
)
UPLOAD_DIR = PATH = os.getcwd() + os.path.expanduser("/uploads")
@router.post("/upload/")
async def upload_images(_user_id: int = Form(...),
    _content_id: int = Form(...), db: Session = Depends(get_db),files: List[UploadFile] = File(...)):

    saved_file_paths = []
    for file in files:
        
        try:
            file_contents = await file.read()
            # 파일 저장 등의 추가 작업
            #print(f"{file_contents} \n {os.path.splitext(file.filename)}")
            _, file_extension = os.path.splitext(file.filename)
            file_name= f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_extension}"
            saved_file_path = os.path.join(UPLOAD_DIR, file_name)  # 이미지를 저장할 경로
            print(saved_file_path)
            with open(saved_file_path, "wb") as f:
                f.write(file_contents)
            saved_file_paths.append(saved_file_path)
            _image_create=ImageCreate(user_id=_user_id,content_id=_content_id)
            print(f"{_image_create} \n{saved_file_path}")
            image_id = image_crud.create_image(db=db,image_create=_image_create,_image_url=saved_file_path)
        except Exception as e:
            print(f"Error reading file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to read file {file.filename}")
        
    return {
        "status_code": status.HTTP_200_OK,
        "detail":"정상적으로 저장되었습니다.",
        "index" : image_id
    }
