#!/usr/bin/env bash
set -euo pipefail

echo "==> Titan API entrypoint"
echo "    Workers: ${WORKERS_COUNT:-auto}"

# Run Alembic migrations when explicitly requested (e.g. first-time setup)
if [[ "${RUN_MIGRATIONS:-false}" == "true" ]]; then
    echo "==> Running database migrations..."
    alembic upgrade head
    echo "==> Migrations complete"
fi

echo "==> Starting application..."
exec "$@"
