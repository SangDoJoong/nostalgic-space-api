from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from user.user_crud import pwd_context
from user import user_crud, user_schema
from dotenv import load_dotenv
import os


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_200_OK)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        return {
            "status_code": status.HTTP_409_CONFLICT,
            "detail": "이미 존재하는 사용자입니다.",
            "data": {
                "username": _user_create.username
            }
        }
    user_crud.create_user(db=db, user_create=_user_create)
    
    return {
        "detail": "정상적으로 생성되었습니다.",
        "data": {
            "username": _user_create.username
        }
    }


@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 혹은 패스워드가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "status_code": status.HTTP_200_OK,
        "detail":"정상적으로 로그인되었습니다.",
        "data":{
            "access_token": access_token,
            "token_type": "bearer",
            "username": user.username,
        }
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = {"username": username}
    except JWTError:
        raise credentials_exception
    else:
        return token_data
    
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    
    return current_user
