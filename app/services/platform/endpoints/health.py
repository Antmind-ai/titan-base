import asyncio
from datetime import UTC, datetime
import time

from fastapi import APIRouter
import psutil

from app.core.cache import check_redis_health
from app.core.config import settings
from app.core.database import check_db_health
from app.services.platform.schemas.health import HealthResponse, HealthStatus, SystemInfo

router = APIRouter()

_start_time = time.monotonic()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service Health Check",
    description="Returns health status of Titan API and all dependencies.",
)
async def health_check() -> HealthResponse:
    db_health, redis_health = await asyncio.gather(
        check_db_health(),
        check_redis_health(),
    )

    all_healthy = db_health["status"] == "healthy" and redis_health["status"] == "healthy"

    return HealthResponse(
        status=HealthStatus.HEALTHY if all_healthy else HealthStatus.DEGRADED,
        service="titan",
        creator="Antmind Ventures Private Limited",
        version=settings.app_version,
        uptime_seconds=round(time.monotonic() - _start_time, 2),
        timestamp=datetime.now(UTC),
        checks={
            "database": db_health,
            "redis": redis_health,
        },
        system=SystemInfo(
            cpu_percent=psutil.cpu_percent(interval=None),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage("/").percent,
        ),
    )
