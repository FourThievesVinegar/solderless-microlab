#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Node.js (v18 LTS)..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get update
apt-get install -y --no-install-recommends nodejs curl

echo "==> Installing Yarn (v1)..."
YARN_VER="1.22.22"
mkdir -p /opt/yarn
curl -L "https://github.com/yarnpkg/yarn/releases/download/v${YARN_VER}/yarn-v${YARN_VER}.tar.gz" \
  | tar xz --strip-components=1 -C /opt/yarn

echo "==> Installing 'serve' via Yarn..."
/opt/yarn/bin/yarn global add serve --prefix /opt/yarn
