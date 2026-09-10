---
title: Microduck
created: 2026-08-30
updated: 2026-08-30
type: entity
tags: [product, press-kit]
sources:
  - raw/articles/microduck-fact-sheet-2026.md
  - raw/articles/workspace-readme-hardware-2026-08-29.md
confidence: high
---

# Microduck

[[pollen-robotics]] / [[hugging-face]] 消费级双足鸭子机器人。预售 $399（2026-08）；软件开源，机械/部分电子不开源。

## 关键规格

| 项 | 值 |
|----|-----|
| 尺寸 | ~25 cm 高 × 14 cm 宽 |
| 重量 | <800 g |
| 电机 | 15× [[dynamixel-xl330]] |
| 主控 | [[radxa-zero-3w]]（1 GB / 32 GB） |
| 传感 | 相机、8×8 ToF、2× IMU、NFC×2 |
| 电池 | [[np-f550-battery]] |

## 板级架构

见 [[board-interconnect]]：[[radxa-zero-3w]] + [[elec-rpi-robot-hat]] + [[imu-to-dxl-v2]]。

## 软件

官方：`microduck`（robotd 等）、`microduck_rl`、`microduck-simulator`。原型作者 [[apirrone]]。仿真摩擦用 [[better-actuator-models-bam]]。

相关：[[opensource-coverage]] · [[firmware-flash-matrix]] · [[local-workspace-layout]]
