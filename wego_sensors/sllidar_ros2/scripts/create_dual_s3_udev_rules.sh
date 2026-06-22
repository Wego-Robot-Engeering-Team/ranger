#!/bin/bash

set -e

FRONT_DEV="${1:-/dev/ttyUSB1}"
REAR_DEV="${2:-/dev/ttyUSB2}"
RULE_PATH="/etc/udev/rules.d/99-sllidar-dual.rules"
TMP_RULE="$(mktemp)"

get_id_path() {
  local dev="$1"
  udevadm info -q property -n "${dev}" | sed -n 's/^ID_PATH=//p' | head -n 1
}

if [ ! -e "${FRONT_DEV}" ]; then
  echo "Front lidar device not found: ${FRONT_DEV}" >&2
  exit 1
fi

if [ ! -e "${REAR_DEV}" ]; then
  echo "Rear lidar device not found: ${REAR_DEV}" >&2
  exit 1
fi

FRONT_ID_PATH="$(get_id_path "${FRONT_DEV}")"
REAR_ID_PATH="$(get_id_path "${REAR_DEV}")"

if [ -z "${FRONT_ID_PATH}" ]; then
  echo "Could not read ID_PATH for ${FRONT_DEV}" >&2
  exit 1
fi

if [ -z "${REAR_ID_PATH}" ]; then
  echo "Could not read ID_PATH for ${REAR_DEV}" >&2
  exit 1
fi

cat > "${TMP_RULE}" <<EOF
# Auto-generated dual S3 rules
# Front lidar: ${FRONT_DEV}
# Rear lidar: ${REAR_DEV}
SUBSYSTEM=="tty", ENV{ID_PATH}=="${FRONT_ID_PATH}", MODE:="0666", SYMLINK+="frontS3"
SUBSYSTEM=="tty", ENV{ID_PATH}=="${REAR_ID_PATH}", MODE:="0666", SYMLINK+="rearS3"
EOF

echo "Installing udev rules to ${RULE_PATH}"
sudo cp "${TMP_RULE}" "${RULE_PATH}"
sudo udevadm control --reload-rules
sudo udevadm trigger

rm -f "${TMP_RULE}"

echo
echo "Created lidar links:"
ls -l /dev/frontS3 /dev/rearS3 2>/dev/null || true
