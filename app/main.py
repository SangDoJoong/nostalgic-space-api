import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import base_router
from api.content import content_router
from api.image import image_router
from api.map import map_router
from api.user import user_router
from config import docs_security
from config.events import shutdown, startup
from config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI()

    # 보안 문서 미들웨어
    app.add_middleware(docs_security.ApidocBasicAuthMiddleware)

    # CORS 설정
    origins = settings.CORS_ORIGINS.split(",")
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


if __name__ == "__main__":
    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
