#!/usr/bin/env bash
set -euo pipefail

# Read solderless-microlab repository tag from arguments
REPO_TAG="$1"

echo "==> Installing prerequisites..."
apt-get update
apt-get install -y --no-install-recommends git

echo "==> Creating default user 'thief'..."
if ! id thief &>/dev/null; then
  useradd -m -s /bin/bash thief
  echo 'thief:vinegard' | chpasswd

  # usermod -a ("append") -G ("supplementary groups")
  # grant access to GPU/input (needed for Xorg)
  usermod -aG video,input,render thief

  # grant sudo and GPIO rights to *thief* user
  usermod -aG sudo thief
  usermod -aG gpio thief
fi

if id pi &>/dev/null; then
  echo "==> Removing default 'pi' user to avoid rename prompt"
  deluser --remove-home pi || true
fi

echo "==> Cloning solderless-microlab into /opt..."
rm -rf /opt/solderless-microlab
git clone --depth 1 --branch "$REPO_TAG" \
  https://github.com/FourThievesVinegar/solderless-microlab.git \
  /opt/solderless-microlab

echo "==> Installing Python 3 stack..."
apt-get install -y python3 python3-pip

echo "==> Installing Chromium browser..."
apt-get install -y chromium

# Delegate XServer installation
bash /tmp/install-x11-kiosk.sh

# Delegate Python Venv installation
bash /tmp/install-venv.sh

# Delegate Node/Yarn setup
bash /tmp/install-node-yarn.sh

# Delegate UI compilation
bash /tmp/compile-ui.sh

# Delegate configuring bootup settings
bash /tmp/block-first-boot-wizards.sh

echo "==> Enabling microlab-firstboot.service..."
mkdir -p /var/lib/microlab/
touch /var/lib/microlab/firstboot.flag

echo "==> Enabling systemd services..."
SYSTEMD_DIR="/etc/systemd/system"
WANTS_DIR="${SYSTEMD_DIR}/multi-user.target.wants"
mkdir -p "$WANTS_DIR"

SERVICES=(
  microlab-backend.service
  microlab-frontend.service
  microlab-browser.service
  microlab-firstboot.service
)

# Symlink each unit into multi-user.target.wants
for svc in "${SERVICES[@]}"; do
  ln -sf "${SYSTEMD_DIR}/${svc}" "${WANTS_DIR}/${svc}"
done

echo "==> Provisioning complete!"
