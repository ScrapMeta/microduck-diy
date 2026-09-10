#!/usr/bin/env bash
# Attach OpenOCD for SWD debug (J2 BM07). Keep this running; GDB connects to :3333.
# Usage (from imu_to_dxl/ or firmware/):
#   ../scripts/debug_openocd.sh
#   gdb-multiarch firmware/build/imu_to_dxl.elf
#     (gdb) target extended-remote localhost:3333
#     (gdb) monitor reset halt
#     (gdb) load
#     (gdb) break main
#     (gdb) continue
set -euo pipefail
exec openocd -f interface/stlink.cfg -f target/stm32g0x.cfg
