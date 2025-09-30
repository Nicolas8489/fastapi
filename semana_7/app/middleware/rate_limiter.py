from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time

class RealRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/real_"):
            return await call_next(request)
        client_ip = request.client.host
        key = f"real_:rate_limit:{client_ip}"
        requests = self.redis.zrangebyscore(key, int(time.time()) - 60, int(time.time()))
        if len(requests) >= 300:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        self.redis.zadd(key, {str(time.time()): time.time()})
        self.redis.expire(key, 60)
        return await call_next(request)
