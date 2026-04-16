from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.config import settings
from src.middleware.rate_limit import limiter
from src.routes import assessments, alerts, facilities, sync, realtime, auth
from src.monitoring.health import router as health_router
import structlog
import time
from starlette.middleware.base import BaseHTTPMiddleware

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

app = FastAPI(title="Golden Hour API", version="1.0.0", docs_url="/api/docs", redoc_url="/api/redoc")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        level = "warning" if duration_ms > 1000 else "info"
        getattr(logger, level)(
            "request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            response_time_ms=duration_ms,
        )
        return response


app.add_middleware(LoggingMiddleware)

app.include_router(health_router)
app.include_router(assessments.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(facilities.router, prefix="/api/v1")
app.include_router(sync.router, prefix="/api/v1")
app.include_router(realtime.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
