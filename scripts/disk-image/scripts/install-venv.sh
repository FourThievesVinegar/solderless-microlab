#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Python Virtual Environment..."
PROJECT_ROOT="/opt/solderless-microlab"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/.venv"
REQ_FILE="$BACKEND_DIR/requirements.txt"

python3 -m venv "$VENV_DIR"
# use the venv's pip to install or upgrade
"$VENV_DIR/bin/pip" install --upgrade -r "$REQ_FILE"
