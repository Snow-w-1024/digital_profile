#!/bin/sh
set -eu

if [ -z "${ADMIN_PASSWORD:-}" ]; then
    echo "ADMIN_PASSWORD must be set" >&2
    exit 1
fi

export ADMIN_HASH="$(python3 tool/passwd.py)"
exec "$@"
