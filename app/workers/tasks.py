from datetime import UTC, datetime
from typing import Any

from loguru import logger


async def health_ping_task(ctx: dict[str, Any], source: str = "api") -> dict[str, str]:
    """Simple ARQ job used to verify worker + Redis wiring."""
    logger.info("ARQ job received | source={}", source)
    return {
        "status": "ok",
        "source": source,
        "processed_at": datetime.now(UTC).isoformat(),
    }
