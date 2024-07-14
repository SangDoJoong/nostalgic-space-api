import datetime
from starlette import status
from pydantic import BaseModel, validator, EmailStr
from fastapi import APIRouter, HTTPException

class ContentCreate(BaseModel):
    title: str
    content: str

    @validator("content", "title", pre=True, always=True)
    def not_empty(cls, v, field):
        if not v or not v.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.name}이(가) 비어있을 수 없습니다."
            )
        return v


 



class Token(BaseModel):
    access_token: str
    token_type: str
    #username: str
