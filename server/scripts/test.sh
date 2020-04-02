#!/bin/sh

set -e

CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BACKEND_DIR="$(dirname "$CURRENT_DIR")"

coverage run --rcfile "${BACKEND_DIR}/pyproject.toml" -m pytest "${BACKEND_DIR}/tests" "$*"
coverage html --rcfile "${BACKEND_DIR}/pyproject.toml"
