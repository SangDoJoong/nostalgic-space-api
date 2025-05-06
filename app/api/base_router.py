from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()


@router.get(
    "/ping",
)
async def ping() -> JSONResponse:
    return JSONResponse(content={"message": "pong"})


@router.get(
    "/docs",
    tags=["documentation"],
    include_in_schema=False,
)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@router.get(
    "/openapi.json",
    tags=["documentation"],
    include_in_schema=False,
)
async def openapi() -> JSONResponse:
    openapi_schema = get_openapi(title="FastAPI", version="0.1.0", routes=router.routes)
    return JSONResponse(content=openapi_schema)


@router.get(
    "/redoc",
    tags=["documentation"],
    include_in_schema=False,
)
async def get_redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="docs")
