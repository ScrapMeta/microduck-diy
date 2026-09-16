---
title: elec_RPI_Robot_HAT
created: 2026-08-30
updated: 2026-09-08
type: entity
tags: [board, hat, power, open-source]
sources:
  - raw/articles/elec-hat-readme-excerpt.md
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/articles/lcsc-hat-bom-order-so26090519869-2026-09-05.md
confidence: high
related: [board-hat, elec-three-boards, board-interconnect, np-f550-battery, opensource-coverage, diy-bom, elec-hat-lcsc-order-2026-09-05, board-imu-to-dxl]
---

# elec_RPI_Robot_HAT（ASE01187-C1）

[[pollen-robotics]] 开源 KiCad 工程：**扩展板 + 电源板一体**。适配 Pi Zero / [[radxa-zero-3w]] 40pin。

> **速查卡：** [[board-hat]] · 电控入口 [[elec-three-boards]] · 接线 [[board-interconnect]]  
> 外形：**65×30.9 mm** · 厚 **1.0 mm** · 与 [[radxa-zero-3w]] 同板框。  
> **DIY 装机：与 Zero 叠装于头部**（非躯干）。

## 功能

- Dynamixel TTL/485（J13/J14 = 3P TTL；Microduck 用 TTL）
- 音频：TLV320AIC3104 + PAM8406 + MEMS 麦 + Wago
- Qwiic/Stemma → 头 ToF
- 板载 BMI088：控制环**不用**（控制用机身 [[imu-to-dxl-v2]] / DIY [[board-imu-to-dxl]]）；**DIY 头 IMU 启用本芯片**
- 供电 **5–28 V**，经电池/电机口进电，AP63205→5V

## 仓库

本地：`refs/elec_RPI_Robot_HAT/`。软件侧设备树写明 “Pollen Robotics RPI Robot HAT”。

## 采购

- 立创订单 **SO26090519869**（2026-09-05）：部分物料 · 到货核对见 [[elec-hat-lcsc-order-2026-09-05]]

相关：[[board-hat]] · [[elec-three-boards]] · [[board-interconnect]] · [[diy-bom]] · [[elec-hat-lcsc-order-2026-09-05]]
