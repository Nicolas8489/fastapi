from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

class RealValidator(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/real_"):
            if datetime.now().hour < 9 or datetime.now().hour > 18:
                raise HTTPException(status_code=403, detail="Fuera de horario")
            if "X-Real-License" not in request.headers:
                raise HTTPException(status_code=400, detail="Header X-Real-License requerido")
        return await call_next(request)
