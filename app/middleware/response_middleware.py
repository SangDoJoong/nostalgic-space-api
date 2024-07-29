# # from fastapi import FastAPI, Request
# # from starlette.middleware.base import BaseHTTPMiddleware
# # from starlette.responses import Response, StreamingResponse
# # import json
# # class ResponseMiddleware(BaseHTTPMiddleware):
# #     async def dispatch(self, request: Request, call_next):
# #         response = await call_next(request)
# #         print(response)
# #         # if isinstance(response, StreamingResponse):
# #         #     print("!")
# #         #     # For streaming responses, we need to capture the chunks, modify them, and re-stream
# #         #     async def stream_response(response):
# #         #         async for chunk in response.body_iterator:
# #         #             # Modify chunk if necessary (for now, we are just passing it through)
# #         #             yield chunk

# #         #     return StreamingResponse(stream_response(response), status_code=response.status_code, headers=dict(response.headers))
        
# #         # else:
# #         print("?")
# #         body = await response.body()
# #         print(body)
# #         response_body = json.loads(body.decode())
# #         modified_body = {"modified": response_body}
# #         return Response(content=json.dumps(modified_body), status_code=response.status_code, headers=dict(response.headers), media_type="application/json")


# import json
# from starlette.middleware.base import BaseHTTPMiddleware
# from starlette.requests import Request
# from starlette.responses import Response, StreamingResponse

# class ResponseMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         response = await call_next(request)

#         if isinstance(response, StreamingResponse):
#             print("?")
#             # For streaming responses, we need to capture the chunks, modify them, and re-stream
#             async def stream_response(response):
#                 async for chunk in response.body_iterator:
#                     # Modify chunk if necessary (for now, we are just passing it through)
#                     yield chunk

#             return StreamingResponse(stream_response(response), status_code=response.status_code, headers=dict(response.headers))
        
#         else:
#             body = await response.body()
#             response_body = json.loads(body.decode())
#             modified_body = {"modified": response_body}
#             print(modified_body)
#             return Response(content=json.dumps(modified_body), status_code=response.status_code, headers=dict(response.headers), media_type="application/json")





import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.types import ASGIApp, Receive, Scope, Send

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if isinstance(response, StreamingResponse):
            # For streaming responses, we need to capture the chunks, modify them, and re-stream
            original_chunks = []
            async for chunk in response.body_iterator:
                original_chunks.append(chunk)
            
            body = b''.join(original_chunks)
            response_body = json.loads(body.decode())
            modified_body = {"modified": response_body}
            modified_content = json.dumps(modified_body).encode()
            
            headers = dict(response.headers)
            headers["Content-Length"] = str(len(modified_content))
            
            print(modified_content)
            
            return StreamingResponse(iter([modified_content]), status_code=response.status_code, headers=headers, media_type="application/json")
        
        else:
            body = await response.body()
            response_body = json.loads(body.decode())
            modified_body = {"modified": response_body}
            modified_content = json.dumps(modified_body).encode()
            
            headers = dict(response.headers)
            headers["Content-Length"] = str(len(modified_content))
            
            return Response(content=modified_content, status_code=response.status_code, headers=headers, media_type="application/json")
