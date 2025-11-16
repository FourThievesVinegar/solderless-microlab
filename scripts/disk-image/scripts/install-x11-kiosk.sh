#!/usr/bin/env bash
set -euo pipefail

# Minimal X + Chromium for kiosk. No display manager.
# Uses existing microlab-browser.service + /opt/solderless-microlab/scripts/startBrowser.sh

KIOSK_USER=thief

echo "==> Installing minimal X stack and Chromium..."
apt-get update
apt-get install -y --no-install-recommends \
  xserver-xorg xinit x11-xserver-utils \
  chromium \
  xdotool \
  unclutter

# Some images name the binary 'chromium' instead of 'chromium-browser'
if ! command -v chromium-browser >/dev/null 2>&1 && command -v chromium >/dev/null 2>&1; then
  ln -sf /usr/bin/chromium /usr/local/bin/chromium-browser
fi

# Make sure your browser script is executable
if [ -f /opt/solderless-microlab/scripts/startBrowser.sh ]; then
  chmod +x /opt/solderless-microlab/scripts/startBrowser.sh
fi

echo "==> install-x11-kiosk: done."
echo "    - X will start on demand via microlab-browser.service"
echo "    - Service will auto-skip if no display is connected (HDMI or DSI/eDP)."
