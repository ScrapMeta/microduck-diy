#!/usr/bin/env bash
# Flash via ST-Link + OpenOCD (SWD on J2 BM07).
# Run from firmware/ (default ELF) or pass absolute/relative path to .elf.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ELF="${1:-$ROOT/firmware/build/imu_to_dxl.elf}"
if [[ ! -f "$ELF" ]]; then
  echo "missing ELF: $ELF (run: cd firmware && make g031)" >&2
  exit 1
fi
openocd -f interface/stlink.cfg -f target/stm32g0x.cfg \
  -c "program ${ELF} verify reset exit"
