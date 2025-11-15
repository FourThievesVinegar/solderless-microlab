#!/usr/bin/env bash
set -euo pipefail

# inspector: mount a Raspberry Pi OS image and drop into a shell
# Usage: inspect-raspios-microlab.sh <path-to-raspios-image>

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-raspios-image>"
  exit 1
fi

IMG="$1"
LOOP_DEV=""

cleanup() {
  echo "Cleaning up..."
  mountpoint -q /mnt/pi-boot && umount /mnt/pi-boot
  mountpoint -q /mnt/pi-root && umount /mnt/pi-root
  if [ -n "$LOOP_DEV" ]; then
    kpartx -d "$LOOP_DEV" || true
    losetup -d "$LOOP_DEV"   || true
  fi
}
trap cleanup EXIT

echo "1) Attaching image to loop device..."
LOOP_DEV=$(losetup --show -f "$IMG")
echo "   -> $LOOP_DEV"

echo "2) Creating partition mappings..."
kpartx -av "$LOOP_DEV"

PREFIX=$(basename "$LOOP_DEV")

echo "3) Mounting partitions..."
mkdir -p /mnt/pi-boot /mnt/pi-root

# Mount the FAT32 boot partition read-only
mount -t vfat -o ro "/dev/mapper/${PREFIX}p1" /mnt/pi-boot
echo "   • Boot -> /mnt/pi-boot"

# Mount the ext4 rootfs read-only, disable journal replay
mount -t ext4 -o ro,noload "/dev/mapper/${PREFIX}p2" /mnt/pi-root
echo "   • Root -> /mnt/pi-root"

cat <<-EOF

=== INSPECTION READY ===

 • Browse boot:  ls /mnt/pi-boot
 • Browse root:  ls /mnt/pi-root

Type 'exit' to quit and trigger cleanup.
EOF

# Drop into a login shell
exec /bin/bash --login
