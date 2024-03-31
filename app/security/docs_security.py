import secrets
from fastapi import FastAPI, HTTPException, status, Depends,APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.utils import  get_openapi

security = HTTPBasic()
router = APIRouter(
    dependencies=[Depends(security)],
)
# 인증정보 
name= "nostel_api"
password="sandojoong"


# User Verification Function
def verification(creds: HTTPBasicCredentials = Depends(security)):

    if creds.username == name and creds.password == password:
        print("User Validated")
        return True
    else:
        # From FastAPI 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
