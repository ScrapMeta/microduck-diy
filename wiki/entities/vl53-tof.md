---
title: VL53 ToF（头 LiDAR）
created: 2026-08-30
updated: 2026-08-30
type: entity
tags: [tof]
sources: [raw/articles/workspace-readme-hardware-2026-08-29.md]
confidence: medium
---

# VL53L5CX / VL53L8CX

头部 8×8 ToF（Press Kit 称 compact LiDAR）。经 [[elec-rpi-robot-hat]] Qwiic/Stemma。`tofd` 每次启动经 I2C 上传约 **90 KB** 固件到传感器 RAM。软件在 `microduck/tof`。

相关：[[board-interconnect]] · [[firmware-flash-matrix]] · [[microduck]]
