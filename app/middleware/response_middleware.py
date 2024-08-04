import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if isinstance(response, StreamingResponse):
            async def stream_response_body(body_iterator):
                async for chunk in body_iterator:
                    yield chunk  # Modify chunk if necessary

            modified_streaming_response = StreamingResponse(
                stream_response_body(response.body_iterator),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
            modified_streaming_response.background = response.background
            return modified_streaming_response

        else:
            body = await response.body()
            try:
                response_body = json.loads(body.decode())
            except json.JSONDecodeError:
                response_body = body.decode()

            modified_body = {
                "status_code": response.status_code,
                "detail": "OK" if response.status_code == 200 else "Error",
                "data": response_body
            }
            modified_response = Response(
                content=json.dumps(modified_body),
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type="application/json"
            )
            return modified_response