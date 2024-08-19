import os

from content import content_router
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from image import image_router
from security import docs_security
from user import user_router

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


@app.get(
    "/docs",
    tags=["documentation"],
    include_in_schema=False,
)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get(
    "/openapi.json",
    tags=["documentation"],
    include_in_schema=False,
)
async def openapi() -> JSONResponse:
    openapi_schema = get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)
    return JSONResponse(content=openapi_schema)


@app.get(
    "/redoc",
    tags=["documentation"],
    include_in_schema=False,
)
async def get_redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


# Include routers
app.include_router(user_router.router)
app.include_router(content_router.router)
app.include_router(image_router.router)
