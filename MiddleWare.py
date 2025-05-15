from starlette.concurrency import iterate_in_threadpool

from helpers.Logging import get_logger
import json
from fastapi import Request, Response

class LoggingMiddleware:

    def __init__(self):
        self.logger = get_logger(__name__)

    async def pretty_body(self, body: bytes, content_type):
    
        if not body:
            return ''
    
        if "application/json" in content_type:
    
            try:
                body = body.decode('utf-8')
                pretty_body = json.dumps(json.loads(body), indent=4)
    
            except Exception as e:
                self.logger.warning(f"Could not decode body: {e}")
                return ''
    
        else:
    
            try:
                pretty_body = body.decode("utf-8")
    
            except Exception as e:
                self.logger.warning(f"Could not decode body: {e}")
                return ''
    
        return pretty_body
    
    
    async def pretty_headers(self, headers):
        return '\n'.join([f'{k}:{v}' for k,v in headers.items()])
    
    
    async def __call__(self, request: Request, call_next):
        message = (
            f'\n\n-----FastAPI Request-----'
            f'\n{request.method} {request.url}'
            f'\n\n{await self.pretty_headers(request.headers)}'
            f'\n\n{await self.pretty_body(await request.body(), request.headers.get("content-type", ""))}'
        )

        self.logger.debug(message)
    
        response: Response = await call_next(request)
    
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))

        message = (
            f'\n\n-----FastAPI Response-----'
            f'\nStatus: {response.status_code}'
            f'\n\n{await self.pretty_headers(response.headers)}'
            f'\n\n{await self.pretty_body(b"".join(response_body), response.headers.get("content-type", ""))}'
        )
        self.logger.debug(message)
    
        return response