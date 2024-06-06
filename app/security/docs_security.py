import base64
import secrets

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from typing import Any, Dict
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='../secret.env')
# 인증정보 
secret_name= os.environ.get("SWAGGER_NAME")

secret_password = os.environ.get("SWAGGER_PASSWORD")

class ApidocBasicAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(  # type: ignore
            self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in ['/docs', '/openapi.json', '/redoc']:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                try:
                    scheme, credentials = auth_header.split()
                    if scheme.lower() == 'basic':
                        
                        decoded = base64.b64decode(credentials).decode('ascii')
                        username, password = decoded.split(':')
                        correct_username = secrets.compare_digest(
                            username, secret_name)
                        
                        correct_password = secrets.compare_digest(
                            password, secret_password)
                        if correct_username and correct_password:
                            return await call_next(request)
                except Exception:
                    ...
            response = Response(content='Unauthorized', status_code=401)
            response.headers['WWW-Authenticate'] = 'Basic'
            return response
        return await call_next(request)