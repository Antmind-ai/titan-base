import time

import redis.asyncio as aioredis
from redis.asyncio import ConnectionPool

from app.core.config import settings

_pool: ConnectionPool | None = None
_client: aioredis.Redis | None = None


async def init_redis() -> None:
    global _pool, _client
    _pool = ConnectionPool.from_url(
        settings.redis_url,
        max_connections=settings.redis_max_connections,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True,
        health_check_interval=30,
    )
    _client = aioredis.Redis(connection_pool=_pool)
    await _client.ping()


async def close_redis() -> None:
    global _pool, _client
    if _client:
        await _client.aclose()
    if _pool:
        await _pool.aclose()
    _client = None
    _pool = None


def get_redis() -> aioredis.Redis:
    if _client is None:
        raise RuntimeError("Redis client not initialized")
    return _client


async def check_redis_health() -> dict:
    start = time.monotonic()
    try:
        await get_redis().ping()
        return {"status": "healthy", "latency_ms": round((time.monotonic() - start) * 1000, 2)}
    except Exception:
        return {"status": "unhealthy", "error": "connection failed"}
