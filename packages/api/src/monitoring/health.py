import time
import redis.asyncio as aioredis
from fastapi import APIRouter
from sqlalchemy import text
from src.database.db import engine
from src.config import settings

router = APIRouter(tags=["health"])
START_TIME = time.time()


@router.get("/health")
async def health_check():
    checks = {}

    try:
        async with engine.connect() as conn:
            t0 = time.monotonic()
            await conn.execute(text("SELECT 1"))
            checks["database"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000, 2)}
    except Exception as e:
        checks["database"] = {"status": "down", "error": str(e)}

    try:
        r = await aioredis.from_url(settings.redis_url)
        t0 = time.monotonic()
        await r.ping()
        await r.aclose()
        checks["redis"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000, 2)}
    except Exception as e:
        checks["redis"] = {"status": "down", "error": str(e)}

    db_ok = checks.get("database", {}).get("status") == "ok"
    redis_ok = checks.get("redis", {}).get("status") == "ok"
    overall = "ok" if db_ok and redis_ok else ("degraded" if db_ok else "down")

    return {
        "status": overall,
        "checks": checks,
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }
