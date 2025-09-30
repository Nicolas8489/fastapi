from fastapi import FastAPI
from .middleware.rate_limiter import RealRateLimiter
from .middleware.logger import RealLogger
from .middleware.validator import RealValidator
from .routers.real_routes import router
from .database.indexes import create_real_indexes
from ..monitoring.metrics import instrumentator, metrics

app = FastAPI(title="API Inmobiliaria - Semana 7")
app.add_middleware(RealValidator)
app.add_middleware(RealLogger)
app.add_middleware(RealRateLimiter)
app.include_router(router)
instrumentator.expose(app)

# Crear índices al iniciar
create_real_indexes(app.state.engine)  # Asegúrate de configurar engine en app.state
