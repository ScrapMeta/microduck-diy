---
title: 固件 / 烧录矩阵
created: 2026-08-30
updated: 2026-09-14
type: concept
tags: [firmware, flash]
sources: [raw/articles/workspace-readme-hardware-2026-08-29.md]
confidence: high
related: [board-imu-to-dxl, imu-to-dxl-firmware-build, imu-to-dxl-v2, opensource-coverage]
---

# 固件 / 烧录矩阵

| 部件 | 要烧吗 | 开源 |
|------|--------|------|
| [[radxa-zero-3w]] | Armbian 系统 | 文档 + seed |
| [[elec-rpi-robot-hat]] | 基本否 | KiCad ✅ |
| [[imu-to-dxl-v2]] | 产线 MCU | 官方 ❌；DIY → `imu_to_dxl/` |
| [[dynamixel-xl330]] | 产线 ID/参数 | 电机属 Robotis |
| [[vl53-tof]] | 每次启动灌 RAM | ✅ tofd |
| 相机/喇叭/麦 | 否 | 驱动/原理图 |

子板与舵机固件 **不进 OTA**（updater-design §11.1）。DIY 机身 IMU：**编译步骤**见 [[imu-to-dxl-firmware-build]]；SWD（J2）烧录见 `imu_to_dxl/scripts/flash_openocd.sh`。

相关：[[board-imu-to-dxl]] · [[imu-to-dxl-firmware-build]] · [[opensource-coverage]] · [[system-flash-armbian]] · [[board-interconnect]]

