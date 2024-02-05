from pydantic import BaseModel, validator, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
