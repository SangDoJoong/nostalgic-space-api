from pydantic import BaseModel, validator, EmailStr
from starlette import status
from fastapi import APIRouter, HTTPException
from typing import Optional

class ImageCreate(BaseModel):
    
    user_id:int
    content_id: Optional[int] = None 
    
    


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
