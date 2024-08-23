import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import HTTPException

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
                return await call_next(request)

            response = await call_next(request)

            if isinstance(response, StreamingResponse):
                body_chunks = []
                async for chunk in response.body_iterator:
                    body_chunks.append(chunk)
                body = b"".join(body_chunks)

                try:
                    response_body = json.loads(body.decode())
                    status_code = response_body.pop("status_code", response.status_code)
                    detail = response_body.pop("detail", "OK" if response.status_code == 200 else "Error")
                    modified_body = {
                        "status_code": status_code,
                        "detail": detail,
                        "data": response_body
                    }
                    modified_body_bytes = json.dumps(modified_body).encode()
                except (json.JSONDecodeError, KeyError, TypeError):
                    modified_body_bytes = body

                async def new_body_iterator():
                    yield modified_body_bytes

                modified_streaming_response = StreamingResponse(
                    new_body_iterator(),
                    status_code=response.status_code,
                    headers={k: v for k, v in response.headers.items() if k.lower() != "content-length"},
                    media_type=response.media_type
                )
                return modified_streaming_response

            else:
                body = await response.body()
                try:
                    response_body = json.loads(body.decode())
                    status_code = response_body.pop("status_code", response.status_code)
                    detail = response_body.pop("detail", "OK" if response.status_code == 200 else "Error")
                except (json.JSONDecodeError, KeyError, TypeError):
                    response_body = body.decode()
                    status_code = response.status_code
                    detail = "OK" if response.status_code == 200 else "Error"

                modified_body = {
                    "status_code": status_code,
                    "detail": detail,
                    "data": response_body
                }
                modified_response = Response(
                    content=json.dumps(modified_body),
                    status_code=status_code,
                    headers={k: v for k, v in response.headers.items() if k.lower() != "content-length"},
                    media_type="application/json"
                )
                return modified_response

        except HTTPException as e:
            return Response(
                content=json.dumps({"status_code": 501, "detail": "Internal Server Error", "data": {}}),
                status_code=501,
                media_type="application/json"
            )

        except Exception as e:
            return Response(
                content=json.dumps({"status_code": 500, "detail": "Internal Server Error", "data": {}}),
                status_code=500,
                media_type="application/json"
            )