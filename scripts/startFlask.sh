#!/usr/bin/env bash
set -euo pipefail

# Guard: require root for the Python process to access GPIO
if [ "$(id -u)" -ne 0 ]; then
  echo "Error: must be run as root or via sudo." >&2
  exit 1
fi

# Deduct the backend directory (where we keep main.py & requirements.txt)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"
VENV_DIR="$BACKEND_DIR/env"
REQ_FILE="$BACKEND_DIR/requirements.txt"

# Create/update venv only if missing or if requirements.txt is newer
if [[ ! -d "$VENV_DIR" ]] || [[ "$REQ_FILE" -nt "$VENV_DIR/bin/activate" ]]; then
  python3 -m venv "$VENV_DIR"
  # use the venv’s pip to install or upgrade
  "$VENV_DIR/bin/pip" install --upgrade -r "$REQ_FILE"
fi

# Enable reading ./backend/defaultconfig.ini
cd "$BACKEND_DIR"

# Launch Flask via the venv’s python interpreter
exec "$VENV_DIR/bin/python" "$BACKEND_DIR/main.py" production
