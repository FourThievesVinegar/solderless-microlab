#!/usr/bin/env bash
set -euo pipefail

# Minimal X + Chromium for kiosk. No display manager.
# Uses existing microlab-browser.service + /opt/solderless-microlab/scripts/startBrowser.sh

KIOSK_USER=thief

echo "==> Installing minimal X stack and Chromium..."
apt-get update
apt-get install -y --no-install-recommends \
  xserver-xorg xinit x11-xserver-utils \
  xdotool \
  unclutter

# udisks2 + gvfs give GIO's volume monitor (used by Chromium's native
# file picker) visibility into removable USB drives, including
# mounting them on click. dbus-bin provides dbus-run-session, used to
# give the kiosk session a D-Bus bus to talk to udisks2 over (see
# microlab-start-browser-session).
apt-get install -y --no-install-recommends \
  udisks2 \
  gvfs gvfs-daemons \
  dbus-bin \
  matchbox-window-manager

# The package name varies by distro/repo: Debian Bookworm's own repos only
# ship 'chromium', while some Raspberry Pi OS repo configs still provide
# the legacy 'chromium-browser' transitional package. Try the modern name
# first so a missing legacy package doesn't hard-fail the whole build.
if apt-get install -y --no-install-recommends chromium; then
  :
elif apt-get install -y --no-install-recommends chromium-browser; then
  :
else
  echo "ERROR: neither 'chromium' nor 'chromium-browser' package is available" >&2
  exit 1
fi

# solderless-microlab's startBrowser.sh invokes the absolute path
# /usr/bin/chromium-browser directly (not just the bare command via
# $PATH), so a symlink anywhere other than /usr/bin is invisible to it.
# Make sure that exact path exists no matter which package landed the
# real binary at /usr/bin/chromium vs /usr/bin/chromium-browser.
if [ ! -e /usr/bin/chromium-browser ] && [ -e /usr/bin/chromium ]; then
  ln -sf /usr/bin/chromium /usr/bin/chromium-browser
fi

if ! command -v /usr/bin/chromium-browser >/dev/null 2>&1; then
  echo "ERROR: /usr/bin/chromium-browser still not present after install/symlink" >&2
  exit 1
fi

# Make sure your browser script is executable
if [ -f /opt/solderless-microlab/scripts/startBrowser.sh ]; then
  chmod +x /opt/solderless-microlab/scripts/startBrowser.sh
fi

echo "==> install-x11-kiosk: done."
echo "    - X will start on demand via microlab-browser.service"
echo "    - Service will auto-skip if no display is connected (HDMI or DSI/eDP)."