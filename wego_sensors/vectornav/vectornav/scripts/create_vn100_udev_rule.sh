#!/bin/bash

set -e

VN_DEV="${1:-/dev/ttyUSB0}"
RULE_PATH="/etc/udev/rules.d/99-vectornav-vn100.rules"
TMP_RULE="$(mktemp)"

get_id_path() {
  local dev="$1"
  udevadm info -q property -n "${dev}" | sed -n 's/^ID_PATH=//p' | head -n 1
}

if [ ! -e "${VN_DEV}" ]; then
  echo "VN100 device not found: ${VN_DEV}" >&2
  exit 1
fi

VN_ID_PATH="$(get_id_path "${VN_DEV}")"

if [ -z "${VN_ID_PATH}" ]; then
  echo "Could not read ID_PATH for ${VN_DEV}" >&2
  exit 1
fi

cat > "${TMP_RULE}" <<EOF
# Auto-generated VectorNav VN100 rule
# Source device: ${VN_DEV}
SUBSYSTEM=="tty", ENV{ID_PATH}=="${VN_ID_PATH}", MODE:="0666", SYMLINK+="vn100"
EOF

echo "Installing udev rule to ${RULE_PATH}"
sudo cp "${TMP_RULE}" "${RULE_PATH}"
sudo udevadm control --reload-rules
sudo udevadm trigger

rm -f "${TMP_RULE}"

echo
echo "Created link:"
ls -l /dev/vn100 2>/dev/null || true
