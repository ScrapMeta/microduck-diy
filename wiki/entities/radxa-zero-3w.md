---
title: Radxa Zero 3W
created: 2026-08-30
updated: 2026-09-05
type: entity
tags: [board, sbc, flash]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/articles/image-readme-seed-2026-08-29.md
confidence: high
related: [board-hat, elec-rpi-robot-hat, elec-three-boards, board-interconnect, radxa, zero3w-bench-plan, system-flash-armbian]
---

# Radxa Zero 3W

Microduck 主控：Rockchip **RK3566**，Wi-Fi/BT，40pin，CSI。跑 **Armbian**。Press Kit：1 GB RAM / 32 GB 存储。早期原型用过 Pi Zero 2W。

**DIY 手头（2026-09-10）：** **2 GB RAM + microSD** 开发板 · 台架规划见 [[zero3w-bench-plan]]。

## 外形

| 项 | 值 |
|----|-----|
| 板框 | **65×30.9 mm**（**6.5×3.09 cm**） |
| 厚度 | **1.0 mm** |
| 与 HAT | **同外形、同板厚**（叠装 40-pin）· [[board-hat]] / [[elec-rpi-robot-hat]] |

参考图：[`assets/pcb/radxa-zero-3w-ref.webp`](../assets/pcb/radxa-zero-3w-ref.webp) · [`radxa-zero-3w-iface.webp`](../assets/pcb/radxa-zero-3w-iface.webp)

## 存储与刷机

- 支持 **microSD** 与板载 **eMMC**
- 量产路径文档写 **eMMC**；开发可 SD 烧录后插板
- 镜像：Armbian Minimal → `provision`；本地 seed：`image/out/`（见 [[system-flash-armbian]] · [[zero3w-bench-plan]]）
- 详见 [[system-flash-armbian]]

## 供电

仅 **5V**（USB 2.0 OTG Type-C）。台架无电池时见 [[bench-power-supply]]。整机经 [[elec-rpi-robot-hat]] 从电池取电再给 5V。

相关：[[board-hat]] · [[elec-three-boards]] · [[microduck]] · [[board-interconnect]] · [[radxa]]
