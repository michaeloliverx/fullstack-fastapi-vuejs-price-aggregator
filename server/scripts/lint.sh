#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BACKEND_DIR="$(dirname "$CURRENT_DIR")"

black --config "${BACKEND_DIR}/pyproject.toml" "${BACKEND_DIR}"
isort --recursive --settings-path "${BACKEND_DIR}/pyproject.toml" "${BACKEND_DIR}"
