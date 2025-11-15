#!/usr/bin/env bash
set -euo pipefail

echo "==> Compiling UI..."
cd /opt/solderless-microlab/gui/
/opt/yarn/bin/yarn install
/opt/yarn/bin/yarn build
