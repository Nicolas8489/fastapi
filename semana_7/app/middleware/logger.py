from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

class RealLogger(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger("real_logger")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("logs/real.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/real_"):
            self.logger.info(f"REQUEST: {request.method} {request.url.path}")
        response = await call_next(request)
        if response.status_code >= 400:
            self.logger.warning(f"RESPONSE: {response.status_code}")
        return response
