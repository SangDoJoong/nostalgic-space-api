
from typing import Any, Dict
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from security import docs_security
from user import user_router
from fastapi.middleware.cors import CORSMiddleware

#from content import content_router
app = FastAPI(docs_url=None, openapi_url=None, redoc_url=None)
app.add_middleware(docs_security.ApidocBasicAuthMiddleware)


origins = [
	"*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    '/docs',
    tags=['documentation'],
    include_in_schema=False,
)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url='/openapi.json', title='docs')


@app.get(
    '/openapi.json',
    tags=['documentation'],
    include_in_schema=False,
)
async def openapi() -> Dict[str, Any]:
    return get_openapi(title='FastAPI', version='0.1.0', routes=app.routes)


@app.get(
    '/redoc',
    tags=['documentation'],
    include_in_schema=False,
)
async def get_redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url='/openapi.json', title='docs')

app.include_router(user_router.router)
#app.include_router(content_router.router)