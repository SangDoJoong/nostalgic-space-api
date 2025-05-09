import base64
import secrets

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from config.settings import settings

secret_name = settings.SWAGGER_NAME
secret_password = settings.SWAGGER_PASSWORD


class ApidocBasicAuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            auth_header = request.headers.get("Authorization")

            if auth_header:
                try:
                    scheme, credentials = auth_header.split()
                    if scheme.lower() == "basic":
                        decoded = base64.b64decode(credentials).decode("ascii")
                        username, password = decoded.split(":")
                        correct_username = secrets.compare_digest(username, secret_name)
                        correct_password = secrets.compare_digest(
                            password, secret_password
                        )

                        if correct_username and correct_password:
                            response = await call_next(request)

                            return response
                except Exception as e:
                    print(f"Exception occurred: {e}")
            response = Response(content="Unauthorized", status_code=401)
            response.headers["WWW-Authenticate"] = "Basic"

            return response
        response = await call_next(request)

        return response
