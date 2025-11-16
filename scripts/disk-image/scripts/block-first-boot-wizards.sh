#!/usr/bin/env bash
set -euo pipefail

echo "==> Removing first-boot flows..."
rm -f /boot/userconf /boot/userconf.txt /boot/rename-user

SYS=/etc/systemd/system

mkdir -p "$SYS"

# Mask the user rename/config service (prevents “which user to rename?” dialog)
ln -sf /dev/null "$SYS/userconfig.service"

# Mask raspi-config firstboot service (prevents keyboard/locale/timezone prompts)
ln -sf /dev/null "$SYS/raspi-config.service"

# Also remove any “wants” symlinks that might start them
rm -f \
  "$SYS/multi-user.target.wants/userconfig.service" \
  "$SYS/multi-user.target.wants/raspi-config.service" \
  "$SYS/default.target.wants/userconfig.service" \
  "$SYS/default.target.wants/raspi-config.service"
