from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends,File ,UploadFile,Form,Query
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from database import get_db
from image import image_crud, image_schema
from image.image_schema import ImageCreate,UserImageCreate,ContentImageCreate
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
router = APIRouter(
    prefix="/api",
)
async def save_file(file: UploadFile, upload_dir: str = "/uploads/") -> str:
    try:
        file_contents = await file.read()
        _, file_extension = os.path.splitext(file.filename)
        file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_extension}"
        saved_file_path = os.path.join(upload_dir, file_name)  # 이미지를 저장할 경로
        with open(saved_file_path, "wb") as f:
            f.write(file_contents)
        return saved_file_path
    except Exception as e:
        print(f"Error reading file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename}")

@router.post("/userimage")
async def upload_user_image(_user_id: int = Form(...), db: Session = Depends(get_db),files: List[UploadFile] = File(...)):

    image_ids = []
    for file in files:
        try:
            saved_file_path = await save_file(file)
            _image_create = ImageCreate(image_address=saved_file_path)
            image_id = image_crud.create_user_image(db=db, image_create=_image_create, user_id=_user_id)
            image_ids.append(image_id)
        except HTTPException as e:
            raise e
        
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 저장되었습니다.",
        "indexes": image_ids
    }

@router.post("/upload/contentimage")
async def upload_images(_user_id: int = Form(...),
    _content_id:  Optional[int]= Form(None), db: Session = Depends(get_db),files: List[UploadFile] = File(...)):

    image_ids = []
    for file in files:
        try:
            saved_file_path = await save_file(file)
            _image_create = ImageCreate(user_id=_user_id, content_id=_content_id)
            image_id = image_crud.create_image(db=db, image_create=_image_create, _image_url=saved_file_path)
            image_ids.append(image_id)
        except HTTPException as e:
            raise e
        
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "정상적으로 저장되었습니다.",
        "indexes": image_ids
    }
@router.get("/userimage")
def get_user_images(_user_id: int = Query(...), db: Session = Depends(get_db)):
    user_images = image_crud.get_user_image(db, _user_id)
    if not user_images:
        raise HTTPException(status_code=404, detail="User images not found")
    return user_images