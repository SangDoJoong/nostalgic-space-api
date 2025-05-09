import argparse
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import base_router
from api.content import content_router
from api.image import image_router
from api.map import map_router
from api.user import user_router
from config import docs_security
from config.events import shutdown, startup
from config.settings import Settings


def create_app() -> FastAPI:
    # 환경 변수 로딩
    app_env = os.getenv("APP_ENV", "local")
    load_dotenv(dotenv_path=f".env.{app_env}", override=True)

    app = FastAPI()

    # 보안 문서 미들웨어
    app.add_middleware(docs_security.ApidocBasicAuthMiddleware)

    # CORS 설정
    origins = os.getenv("CORS_ORIGINS", "").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    app.include_router(base_router.router)
    app.include_router(user_router.router)
    app.include_router(content_router.router)
    app.include_router(image_router.router)
    app.include_router(map_router.router)

    # 이벤트 핸들러 등록
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)

    return app


app = create_app()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-env", "--APP_ENV", type=str, default="local")
    args = parser.parse_args()

    os.environ["APP_ENV"] = args.APP_ENV
    print(f"APP_ENV: {args.APP_ENV}")

    load_dotenv(dotenv_path=f".env.{args.APP_ENV}", override=True)
    print(f".env.{args.APP_ENV} loaded")

    settings = Settings()

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
