#!/usr/bin/env bash
set -euo pipefail

# Ensure the script is running as root (or via sudo)
if [ "$(id -u)" -ne 0 ]; then
  echo >&2 "ERROR: This script must be run as root. Try:"
  echo >&2 "  sudo $0 $*"
  exit 1
fi

# --- VARIABLES ---
# assume we started in /workspace
WORKDIR="$(pwd)"
BUILD_DIR="$WORKDIR/build"

MNT_DIR="$BUILD_DIR/mnt"
BASE_IMG_XZ="$BUILD_DIR/raspios-lite.img.xz"
OUTPUT_IMG="$BUILD_DIR/raspios-microlab.img"
RASPBIAN_URL="https://downloads.raspberrypi.org/raspios_lite_arm64_latest"
MICROLAB_TAG="${1:-main}" # Use the first argument as the tag, default to "main"

# 1. Prepare
mkdir -p "$BUILD_DIR"
if [ -f "$BASE_IMG_XZ" ]; then
  echo "==> Using cached OS image: $BASE_IMG_XZ"
else
  echo "==> Downloading Raspberry Pi OS..."
  curl -L "$RASPBIAN_URL" -o "$BASE_IMG_XZ"
fi

echo "==> Decompressing .img.xz archive..."
# requires xz-utils in the builder image
xz --decompress --keep --force --verbose "$BASE_IMG_XZ"
BASE_IMG_RAW="${BASE_IMG_XZ%.img.xz}.img"

echo "==> Expanding image file to 6 GiB"
truncate -s 6G "$BASE_IMG_RAW"

# 2. Setup loop devices & mount
echo "==> Setting up loop device"
LOOPDEV=$(losetup --show -f "$BASE_IMG_RAW")

echo "==> Resizing partition 2 to fill the expanded image"
parted --script "$LOOPDEV" resizepart 2 100%

# ensure the kernel sees the partitions
echo "==> Creating partition mappings with kpartx"
kpartx -a "$LOOPDEV"

# `${LOOPDEV##*/}` is e.g. "loop3"
DEV_NAME=$(basename "$LOOPDEV")
BOOT_PART="/dev/mapper/${DEV_NAME}p1"
ROOT_PART="/dev/mapper/${DEV_NAME}p2"

# 3. Resize the root filesystem to fill the partition**
echo "==> Checking filesystem on $ROOT_PART"
e2fsck -f -p "$ROOT_PART"

echo "==> Resizing $ROOT_PART to use all available space"
resize2fs "$ROOT_PART"

# 4. Mount Raspberry Pi boot and root partitions
echo "==> Mounting Raspberry Pi boot and root partitions..."
mkdir -p "$MNT_DIR/boot" "$MNT_DIR/root"
mount "$BOOT_PART" "$MNT_DIR/boot"
mount "$ROOT_PART" "$MNT_DIR/root"

# 5. Apply overlays
echo "==> Applying bootloader configs..."
cp -r "$WORKDIR/config/"* "$MNT_DIR/boot/"

# --- FIX: sanitize cmdline.txt so boot isn't hijacked by firstboot/kernel cmdline ---
CMDLINE_FILE="$MNT_DIR/boot/cmdline.txt"
if [ -f "$CMDLINE_FILE" ]; then
  echo "==> Sanitizing cmdline.txt (remove firstboot/systemd.run overrides; ensure single line)"
  # Remove Raspberry Pi Imager firstboot override, if present
  sed -i -E 's#\s*init=/usr/lib/raspberrypi-sys-mods/firstboot##' "$CMDLINE_FILE"
  # Remove any leftover systemd.run arguments that would generate kernel-command-line.service
  sed -i -E 's#\s*systemd\.run=[^ ]+##g; s#\s*systemd\.run_[^=]+=[^ ]+##g' "$CMDLINE_FILE"
  # Ensure cmdline is a single, space-delimited line with no leading/trailing spaces
  tr '\n' ' ' < "$CMDLINE_FILE" | tr -s ' ' | sed -e 's/^ *//' -e 's/ *$//' > "$CMDLINE_FILE.tmp"
  mv "$CMDLINE_FILE.tmp" "$CMDLINE_FILE"
fi
# --- end FIX ---

# --- enable SSH ---
touch "$MNT_DIR/boot/ssh"

echo "==> Overlaying root filesystem..."
cp -r "$WORKDIR/overlays/rootfs-overlay/"* "$MNT_DIR/root"

# 6. Chroot + provisioning
echo "==> Copying QEMU and provisioning script..."
mkdir -p "$MNT_DIR/root/usr/bin"
mkdir -p "$MNT_DIR/root/tmp"

cp /usr/bin/qemu-aarch64-static "$MNT_DIR/root/usr/bin/"
cp "$WORKDIR/scripts/configure-microlab.sh" "$MNT_DIR/root/tmp/"
cp "$WORKDIR/scripts/install-venv.sh"  "$MNT_DIR/root/tmp/"
cp "$WORKDIR/scripts/install-x11-kiosk.sh"  "$MNT_DIR/root/tmp/"
cp "$WORKDIR/scripts/install-node-yarn.sh"  "$MNT_DIR/root/tmp/"
cp "$WORKDIR/scripts/compile-ui.sh"  "$MNT_DIR/root/tmp/"
cp "$WORKDIR/scripts/block-first-boot-wizards.sh"  "$MNT_DIR/root/tmp/"

echo "==> Preparing chroot mount namespace (/proc, /sys, /dev)..."
# Create targets (may already exist and be non-empty; that's fine)
for d in proc sys dev dev/pts; do
  mkdir -p "$MNT_DIR/root/$d"
done
# Optional: warn if /proc or /sys have contents; bind-mount will cover them
for d in proc sys; do
  if ! mountpoint -q "$MNT_DIR/root/$d" && [ -n "$(ls -A "$MNT_DIR/root/$d" 2>/dev/null)" ]; then
    echo "WARN: $MNT_DIR/root/$d has contents; bind-mounting over it." >&2
  fi
done

# Mount namespace pieces idempotently
mountpoint -q "$MNT_DIR/root/proc"    || mount -t proc proc "$MNT_DIR/root/proc"
mountpoint -q "$MNT_DIR/root/sys"     || mount --rbind /sys "$MNT_DIR/root/sys"
mountpoint -q "$MNT_DIR/root/dev"     || mount --rbind /dev "$MNT_DIR/root/dev"
mountpoint -q "$MNT_DIR/root/dev/pts" || mount --rbind /dev/pts "$MNT_DIR/root/dev/pts"

echo "==> Entering chroot to provision image..."
chroot "$MNT_DIR/root" /bin/bash -lc "bash /tmp/configure-microlab.sh $MICROLAB_TAG"

# 7. Teardown
echo "==> Cleaning up chroot mount namespace"
# Unmount in reverse order; tolerate rbinds and busy handles
umount -R "$MNT_DIR/root/dev/pts" 2>/dev/null || umount -l "$MNT_DIR/root/dev/pts" || true
umount -R "$MNT_DIR/root/dev"     2>/dev/null || umount -l "$MNT_DIR/root/dev"     || true
umount -R "$MNT_DIR/root/sys"     2>/dev/null || umount -l "$MNT_DIR/root/sys"     || true
umount    "$MNT_DIR/root/proc"    2>/dev/null || umount -l "$MNT_DIR/root/proc"    || true

echo "==> Cleaning up mounts"
umount "$MNT_DIR/boot" "$MNT_DIR/root"
echo "==> Removing partition mappings"
kpartx -d "$LOOPDEV"
losetup -d "$LOOPDEV"

# 8. Finalize
mv "$BASE_IMG_RAW" "$OUTPUT_IMG"
echo "==> Built image at: $OUTPUT_IMG"
