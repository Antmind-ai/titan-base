from collections.abc import Callable
import time
import uuid

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start = time.monotonic()

        request.state.request_id = request_id

        response = await call_next(request)

        duration_ms = (time.monotonic() - start) * 1000

        logger.info(
            "[{rid}] {method} {path} → {status} ({duration:.1f}ms)",
            rid=request_id[:8],
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration=duration_ms,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

        # Also publish timing in a standards-based header for tooling compatibility.
        timing_metric = f"app;dur={duration_ms:.2f}"
        existing_server_timing = response.headers.get("Server-Timing")
        if existing_server_timing:
            response.headers["Server-Timing"] = f"{existing_server_timing}, {timing_metric}"
        else:
            response.headers["Server-Timing"] = timing_metric

        return response
