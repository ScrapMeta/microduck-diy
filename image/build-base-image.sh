#!/usr/bin/env bash
# Build a Microduck Zero 3W *seed* image from Armbian + this repo's board scripts.
# Run on Linux or WSL2 with sudo. Does not need a physical Radxa for the seed bake.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
DUCK_REPO_ROOT=${DUCK_REPO_ROOT:-$(cd "$SCRIPT_DIR/../../microduck" && pwd)}
OUT_DIR=${OUT_DIR:-"$SCRIPT_DIR/out"}
WORK=${WORK:-"$OUT_DIR/work"}
OVERLAY=${OVERLAY:-"$SCRIPT_DIR/overlay"}

# Vendor 6.1 + Debian trixie — matches setup-board audio + setup-gstreamer docs.
# Docs cite 26.2.1; Tuna currently mirrors 26.8.1 with the same combo (reachable in CN).
ARMBIAN_NAME=${ARMBIAN_NAME:-Armbian_26.8.1_Radxa-zero3_trixie_vendor_6.1.115_minimal.img.xz}
ARMBIAN_URL=${ARMBIAN_URL:-https://mirrors.tuna.tsinghua.edu.cn/armbian-releases/radxa-zero3/archive/${ARMBIAN_NAME}}
ARMBIAN_URL_FALLBACK=${ARMBIAN_URL_FALLBACK:-https://mirrors.ustc.edu.cn/armbian-releases/radxa-zero3/archive/${ARMBIAN_NAME}}
ARMBIAN_URL_FALLBACK2=${ARMBIAN_URL_FALLBACK2:-https://dl.armbian.com/radxa-zero3/archive/${ARMBIAN_NAME}}

STAMP=$(date -u +%Y%m%d)
OUT_NAME="microduck-zero3-${STAMP}-seed.img"
KEEP_RAW=${KEEP_RAW:-0}

need() { command -v "$1" >/dev/null 2>&1 || { echo "need $1" >&2; exit 1; }; }
need curl
need xz
need losetup
need mount
need findmnt
need sha256sum
need xxd

if [ "$(id -u)" -ne 0 ]; then
  echo "re-exec with sudo..."
  exec sudo -E env "PATH=$PATH" bash "$0" "$@"
fi

mkdir -p "$OUT_DIR" "$WORK"
cd "$WORK"

echo "==> source tree: $DUCK_REPO_ROOT"
test -f "$DUCK_REPO_ROOT/scripts/setup-board.sh"
test -f "$DUCK_REPO_ROOT/scripts/provision.sh"

download_base() {
  if [ -f "$ARMBIAN_NAME" ]; then
    echo "==> using cached $ARMBIAN_NAME"
    return 0
  fi
  echo "==> downloading $ARMBIAN_NAME"
  local url
  for url in "$ARMBIAN_URL" "$ARMBIAN_URL_FALLBACK" "$ARMBIAN_URL_FALLBACK2"; do
    echo "    try $url"
    if curl -fL --connect-timeout 30 --retry 5 --retry-delay 5 \
        --speed-time 120 --speed-limit 1000 \
        -o "$ARMBIAN_NAME.partial" "$url"; then
      magic=$(xxd -p -l 4 "$ARMBIAN_NAME.partial" 2>/dev/null || true)
      size=$(stat -c%s "$ARMBIAN_NAME.partial" 2>/dev/null || echo 0)
      echo "    magic=$magic size=$size"
      if [ "$magic" = "fd377a58" ] && [ "$size" -gt 50000000 ]; then
        mv "$ARMBIAN_NAME.partial" "$ARMBIAN_NAME"
        return 0
      fi
      echo "    rejecting non-image payload"
    fi
    rm -f "$ARMBIAN_NAME.partial"
  done
  echo "download failed for all mirrors" >&2
  exit 1
}

download_base

RAW=${ARMBIAN_NAME%.xz}
if [ ! -f "$RAW" ]; then
  echo "==> decompress"
  xz -T0 -dk "$ARMBIAN_NAME"
fi

SEED_RAW="$OUT_DIR/$OUT_NAME"
echo "==> copy base -> $SEED_RAW"
cp -f "$RAW" "$SEED_RAW"

cleanup() {
  set +e
  if [ -n "${MNT:-}" ]; then
    sync
    umount -R "$MNT" 2>/dev/null || true
  fi
  if [ -n "${LOOP:-}" ]; then
    losetup -d "$LOOP" 2>/dev/null || true
  fi
}
trap cleanup EXIT

echo "==> losetup"
LOOP=$(losetup -f --show -P "$SEED_RAW")
echo "    $LOOP"
sleep 1
lsblk "$LOOP"

# Prefer partition with /etc; Armbian Zero3 is usually p1=boot FAT, p2=root ext4
# or a single ext4 with /boot.
MNT="$WORK/mnt"
mkdir -p "$MNT"
ROOT_PART=""
BOOT_PART=""

for part in "${LOOP}p2" "${LOOP}p1" "${LOOP}"; do
  [ -b "$part" ] || continue
  if mount -o rw "$part" "$MNT" 2>/dev/null; then
    if [ -d "$MNT/etc" ]; then
      ROOT_PART=$part
      echo "==> rootfs on $part"
      break
    fi
    umount "$MNT"
  fi
done
[ -n "$ROOT_PART" ] || { echo "could not find rootfs partition" >&2; exit 1; }

# Separate /boot?
if [ ! -d "$MNT/boot" ] || [ ! -e "$MNT/boot/armbianEnv.txt" ]; then
  for part in "${LOOP}p1" "${LOOP}p2"; do
    [ -b "$part" ] || continue
    [ "$part" = "$ROOT_PART" ] && continue
    mkdir -p "$MNT/boot"
    if mount -o rw "$part" "$MNT/boot" 2>/dev/null; then
      if [ -e "$MNT/boot/armbianEnv.txt" ] || [ -d "$MNT/boot/dtb" ] || ls "$MNT/boot/"*.dtb >/dev/null 2>&1; then
        BOOT_PART=$part
        echo "==> /boot on $part"
        break
      fi
      umount "$MNT/boot"
    fi
  done
fi

echo "==> inject /opt/microduck"
rm -rf "$MNT/opt/microduck"
mkdir -p "$MNT/opt/microduck"
cp -a "$DUCK_REPO_ROOT/scripts" "$MNT/opt/microduck/"
cp -a "$DUCK_REPO_ROOT/deploy" "$MNT/opt/microduck/"
# Drop huge/irrelevant bits if any
rm -rf "$MNT/opt/microduck/scripts/__pycache__" 2>/dev/null || true

echo "==> inject overlay"
# Ensure LF scripts
find "$OVERLAY" -type f \( -name '*.sh' -o -path '*/sbin/*' \) -exec sed -i 's/\r$//' {} +
cp -a "$OVERLAY/." "$MNT/"
chmod 755 "$MNT/usr/local/sbin/microduck-firstboot"
mkdir -p "$MNT/etc/microduck"
cp -f "$OVERLAY/boot/microduck.env.example" "$MNT/boot/microduck.env.example" 2>/dev/null \
  || cp -f "$SCRIPT_DIR/overlay/boot/microduck.env.example" "$MNT/boot/microduck.env.example"

# Enable firstboot unit (still gated on /boot/microduck.env existing)
if [ -d "$MNT/etc/systemd/system/multi-user.target.wants" ] || mkdir -p "$MNT/etc/systemd/system/multi-user.target.wants"; then
  ln -sfn /etc/systemd/system/microduck-firstboot.service \
    "$MNT/etc/systemd/system/multi-user.target.wants/microduck-firstboot.service"
fi

echo "==> patch armbianEnv (uart + overlay_prefix)"
ENV_TXT="$MNT/boot/armbianEnv.txt"
if [ -f "$ENV_TXT" ]; then
  if grep -Eq '^overlay_prefix=rk35xx$' "$ENV_TXT"; then
    sed -i 's/^overlay_prefix=rk35xx$/overlay_prefix=rk3568/' "$ENV_TXT"
  elif ! grep -Eq '^overlay_prefix=' "$ENV_TXT"; then
    echo 'overlay_prefix=rk3568' >>"$ENV_TXT"
  fi
  if ! grep -Eq '^overlays=' "$ENV_TXT"; then
    echo 'overlays=uart2-m0' >>"$ENV_TXT"
  elif ! grep -E '^overlays=' "$ENV_TXT" | grep -qw uart2-m0; then
    sed -i 's/^overlays=\(.*\)$/overlays=\1 uart2-m0/' "$ENV_TXT"
  fi
  echo "---- armbianEnv.txt ----"
  cat "$ENV_TXT"
else
  echo "WARN: no $ENV_TXT — skip boot patch"
fi

echo "==> mirror camera dtbo under rk3568- prefix"
cam=radxa-zero3-rpi-camera-v2
dtbo_dir=$(find "$MNT/boot" -type d -path '*/rockchip/overlay' 2>/dev/null | head -1 || true)
if [ -n "$dtbo_dir" ] && [ -f "$dtbo_dir/${cam}.dtbo" ]; then
  cp -f "$dtbo_dir/${cam}.dtbo" "$dtbo_dir/rk3568-${cam}.dtbo"
  if [ -f "$ENV_TXT" ]; then
    if ! grep -E '^overlays=' "$ENV_TXT" | grep -qw "$cam"; then
      sed -i "s/^overlays=\(.*\)\$/overlays=\1 ${cam}/" "$ENV_TXT"
    fi
  fi
  echo "    mirrored in $dtbo_dir"
else
  echo "WARN: camera dtbo not found under /boot (ok on some Armbian layouts)"
fi

echo "==> ToF udev rule"
mkdir -p "$MNT/etc/udev/rules.d"
cat >"$MNT/etc/udev/rules.d/99-robot-i2c-pihat.rules" <<'EOF'
SUBSYSTEM=="i2c-dev", KERNELS=="fe5c0000.i2c", SYMLINK+="i2c-pihat"
SUBSYSTEM=="i2c-dev", ATTR{name}=="i2c-gpio-pihat", SYMLINK+="i2c-pihat"
EOF

echo "==> seed marker"
mkdir -p "$MNT/etc/microduck"
cat >"$MNT/etc/microduck/seed-image" <<EOF
name=$OUT_NAME
built_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
base=$ARMBIAN_NAME
duck_scripts=$(cd "$DUCK_REPO_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo unknown)
EOF

sync
cleanup
trap - EXIT

XZ_OUT="$OUT_DIR/${OUT_NAME}.xz"
echo "==> compress $XZ_OUT"
# -6 is enough for a seed; -9e on a 9p/Windows mount can take hours.
xz -T0 -f -k -6 "$SEED_RAW" || xz -T0 -f -k "$SEED_RAW"
# xz -k keeps raw; move .xz next to it
if [ -f "${SEED_RAW}.xz" ]; then
  mv -f "${SEED_RAW}.xz" "$XZ_OUT"
fi

(
  cd "$OUT_DIR"
  sha256sum "$(basename "$XZ_OUT")" >"$(basename "$XZ_OUT").sha256"
)

if [ "$KEEP_RAW" != 1 ]; then
  rm -f "$SEED_RAW"
fi

echo
echo "DONE"
echo "  $XZ_OUT"
cat "$XZ_OUT.sha256"
echo
echo "Flash with Armbian imager / balenaEtcher / dd, then provision:"
echo "  sudo sh /opt/microduck/scripts/provision.sh"
