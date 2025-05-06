import argparse
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.content import content_router
from api.image import image_router
from api.map import map_router
from api.user import user_router
from app.api import base_router
from config import docs_security

# from config.database_init import conn
from config.settings import Settings

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(docs_security.ApidocBasicAuthMiddleware)

# Set CORS origins from environment variable
origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(base_router.router)
app.include_router(user_router.router)
app.include_router(content_router.router)
app.include_router(image_router.router)
app.include_router(map_router.router)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-env", "--APP_ENV", type=str, default="local")
    args = parser.parse_args()

    os.environ["APP_ENV"] = args.APP_ENV
    settings = Settings()

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# DB 연결
# @app.on_event("startup")
# def on_startup():
#     # connetion.py에 선언해준 conn함수를 실행시켜 DB를 연결해준다.
#     conn()
