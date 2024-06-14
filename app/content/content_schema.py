import datetime
from starlette import status
from pydantic import BaseModel, validator, EmailStr
from fastapi import APIRouter, HTTPException

class ContentCreate(BaseModel):
    title : str 
    content: str
    writer_id : int
    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="글이 없는 컨텐츠는 허용되지 않습니다."
            )
        return v
    @validator("title")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="제목이 없는 컨텐츠는 허용되지 않습니다."
            )
        return v


 



class Token(BaseModel):
    access_token: str
    token_type: str
    #username: str
