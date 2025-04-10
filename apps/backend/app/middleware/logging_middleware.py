import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Log request details
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} {response.status_code} "
            f"Completed in {process_time:.4f}s"
        )
        
        return response

