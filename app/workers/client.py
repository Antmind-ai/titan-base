from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

from app.core.config import settings

_pool: ArqRedis | None = None


def _redis_settings() -> RedisSettings:
    return RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        database=settings.redis_db,
    )


async def init_arq_pool() -> None:
    global _pool
    if _pool is None:
        _pool = await create_pool(_redis_settings())


async def close_arq_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None


async def get_arq_pool() -> ArqRedis:
    if _pool is None:
        await init_arq_pool()
    if _pool is None:
        raise RuntimeError("ARQ pool not initialized")
    return _pool


async def enqueue_job(function_name: str, *args: object, **kwargs: object) -> str:
    redis = await get_arq_pool()
    kwargs.setdefault("_queue_name", settings.arq_queue_name)
    job = await redis.enqueue_job(function_name, *args, **kwargs)
    if job is None:
        raise RuntimeError(f"Failed to enqueue ARQ job: {function_name}")
    return job.job_id
