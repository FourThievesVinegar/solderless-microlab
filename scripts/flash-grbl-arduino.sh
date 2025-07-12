#!/bin/bash

# Exit if not run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run with sudo or as root."
   exit 1
fi

echo "Running with sudo privileges."

# Step 1: Install avrdude and wget if not already installed
echo "Checking for required packages..."

MISSING_PACKAGES=()

if ! command -v avrdude &> /dev/null; then
    MISSING_PACKAGES+=(avrdude)
fi

if ! command -v wget &> /dev/null; then
    MISSING_PACKAGES+=(wget)
fi

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo "Installing missing packages: ${MISSING_PACKAGES[@]}"
    apt update
    apt install -y "${MISSING_PACKAGES[@]}"
else
    echo "All required packages are already installed."
fi

# Step 2: Create udev rule for Arduino symlink
UDEV_RULES_FILE="/etc/udev/rules.d/99-microlab.rules"

if [[ ! -f "$UDEV_RULES_FILE" ]]; then
    echo "Creating udev rules for Arduino USB devices..."
    cat <<EOF > "$UDEV_RULES_FILE"
# Give the CH340 clone a non-default priority of 10
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="arduino_usb", OPTIONS+="link_priority=10"

# Give the official Arduino Uno a higher priority so it wins the link
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0043", SYMLINK+="arduino_usb", OPTIONS+="link_priority=20"

SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="5523", SYMLINK+="thermometer_usb"
EOF
    udevadm control --reload-rules
    udevadm trigger
else
    echo "udev rules file already exists: $UDEV_RULES_FILE"
fi

# Step 3: Download GRBL .hex file
GRBL_HEX="grbl.hex"
GRBL_URL="https://github.com/gnea/grbl/releases/download/v1.1h.20190825/grbl_v1.1h.20190825.hex"

echo "Downloading GRBL firmware..."
wget -O "$GRBL_HEX" "$GRBL_URL"

if [[ ! -f "$GRBL_HEX" ]]; then
    echo "Failed to download GRBL firmware."
    exit 1
fi

# Step 4: Check for /dev/arduino_usb
DEV_TTY_ARDUINO="/dev/arduino_usb"

if [[ ! -e "$DEV_TTY_ARDUINO" ]]; then
    echo "Could not find device at $DEV_TTY_ARDUINO. Make sure the Arduino is connected and udev rules are applied."
    exit 1
else
    echo "Arduino detected at $DEV_TTY_ARDUINO"
fi

# Step 5: Flash GRBL to Arduino Uno
echo "Flashing GRBL to Arduino Uno..."
avrdude -v -patmega328p -carduino -P "$DEV_TTY_ARDUINO" -b115200 -D -Uflash:w:$GRBL_HEX:i

if [[ $? -eq 0 ]]; then
    echo "GRBL firmware flashed successfully!"
else
    echo "Flashing failed."
    exit 1
fi
