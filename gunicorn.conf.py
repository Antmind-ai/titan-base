import multiprocessing
import os

# ── Bind ──────────────────────────────────────────────────────────────────────
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# ── Workers ───────────────────────────────────────────────────────────────────
# UvicornWorker = fully async; (2 x cores)+1 is the standard formula.
_default_workers = (2 * multiprocessing.cpu_count()) + 1
_workers_env = int(os.environ.get("WORKERS_COUNT", 0))
workers = _workers_env if _workers_env > 0 else _default_workers
worker_class = "uvicorn.workers.UvicornWorker"

# Recycle workers periodically to prevent memory creep
max_requests = 10_000
max_requests_jitter = 1_000

# ── Timeouts ──────────────────────────────────────────────────────────────────
timeout = 120
graceful_timeout = 30
keepalive = 5

# ── Logging ───────────────────────────────────────────────────────────────────
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()

# ── Process ───────────────────────────────────────────────────────────────────
proc_name = "titan"
daemon = False
preload_app = False # Each worker imports the app separately

# ── Security ──────────────────────────────────────────────────────────────────
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
forwarded_allow_ips = "*"
