from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse
import json

class ResponseMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        if isinstance(response, StreamingResponse):
            async def stream_response(response):
                async for chunk in response.body_iterator:
                    # 여기서 chunk를 원하는 방식으로 처리
                    pass  
            
            await stream_response(response)
            
        else:
            body = await response.body()

            # JSON 파싱 및 수정
            response_body = json.loads(body.decode())
            modified_body = {"modified": response_body}

            # 수정된 JSON을 다시 응답으로 설정
            return Response(content=json.dumps(modified_body), status_code=response.status_code, headers=dict(response.headers), media_type="application/json")
        
        # 수정하지 않은 경우 그대로 반환
        return response