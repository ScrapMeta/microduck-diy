---
title: 双 IMU 选型（现行定稿）
created: 2026-09-01
updated: 2026-09-10
type: concept
tags: [imu, board, open-source]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - concepts/board-interconnect.md
  - concepts/board-imu-to-dxl.md
confidence: high
related:
  - elec-three-boards
  - board-interconnect
  - board-imu-to-dxl
  - board-hat
  - imu-to-dxl-v2
  - elec-rpi-robot-hat
---

# 双 IMU 选型（现行定稿）

> 装机拓扑：[[board-interconnect]] · 板表：[[elec-three-boards]]。

## 0. DIY 定稿

| 角色 | 选用 |
|------|------|
| **控制环 / 机身** | [[board-imu-to-dxl]] **1 号或 2 号**（测试，ID 200；不同时上机） |
| **头姿 / 辅助** | [[board-hat]] 板载 **BMI088** |
| **主控位置** | 头舱：Zero 3W + HAT |

| 测试板 | 外形 | 功能 | DXL | 固定 |
|--------|------|------|-----|------|
| **1 号** | **32×22** | 完整 | 2× 3P | 四角 φ2.2 · 孔距 29 / 19 |
| **2 号** | **22×15** | 简化 | 1× 3P | 两边中心 M2 |

默认 PHY **SN74LVC1G125**。Press Kit 虽写整机双 IMU；控制路径**只认**机身 DXL ID **200**。

## 1. 契约摘要（机身）

| 项 | 值 |
|----|-----|
| 总线 | Protocol 2.0 TTL，ID **200** |
| 控制环读取 | 地址 **124** 起 **12 字节** |
| 0..6 | gyro xyz，`i16` LE，**±500 dps** |
| 6..12 | SFLP quat x/y/z，**IEEE half**；`w=√(1−x²−y²−z²)` |
| 安装 | 两髋上方中间；姿态标定仍须对齐 trunk 约定 |

主机**不做**融合——SFLP（或等价）须在机身板端。

## 2. 决策摘要

1. 机身：先打 **1 号 + 2 号** 对比；上机只挂一块。  
2. 头部：HAT BMI088。  
3. 控制只认 ID 200 · PHY 1G125。

相关：[[imu-to-dxl-v2]] · [[elec-rpi-robot-hat]] · [[board-interconnect]] · [[diy-bom]]
