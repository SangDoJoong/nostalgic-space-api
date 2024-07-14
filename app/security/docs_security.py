import base64
import secrets
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from dotenv import load_dotenv
import os

load_dotenv()

secret_name = os.environ.get("SWAGGER_NAME")
secret_password = os.environ.get("SWAGGER_PASSWORD")

class ApidocBasicAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        print(f"Request URL: {request.url.path}")
        if request.url.path in ['/docs', '/openapi.json', '/redoc']:
            auth_header = request.headers.get('Authorization')
            print(f"Authorization Header: {auth_header}")
            if auth_header:
                try:
                    scheme, credentials = auth_header.split()
                    if scheme.lower() == 'basic':
                        decoded = base64.b64decode(credentials).decode('ascii')
                        username, password = decoded.split(':')
                        correct_username = secrets.compare_digest(username, secret_name)
                        correct_password = secrets.compare_digest(password, secret_password)
                        print(f"Username: {username}, Password: {password}, Correct: {correct_username and correct_password}")
                        if correct_username and correct_password:
                            response = await call_next(request)
                            print(f"Response Status: {response.status_code}")
                            return response
                except Exception as e:
                    print(f"Exception occurred: {e}")
            response = Response(content='Unauthorized', status_code=401)
            response.headers['WWW-Authenticate'] = 'Basic'
            print("Returning 401 Unauthorized")
            return response
        response = await call_next(request)
        print(f"Final Response Status: {response.status_code}")
        return response
