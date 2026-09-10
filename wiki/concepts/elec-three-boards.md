---
title: DIY 电控板速查（HAT · 机身 IMU · 头 IMU）
created: 2026-09-05
updated: 2026-09-09
type: concept
tags: [board, hat, imu, diy, index]
confidence: high
related:
  - board-hat
  - board-imu-to-dxl
  - radxa-zero-3w
  - elec-three-board-bom
  - board-interconnect
  - diy-bom
  - dual-imu-board-selection
---

# DIY 电控板速查

> **定稿 2026-09-09。** 接线：[[board-interconnect]]；采购：[[diy-bom]]。  
> 头舱 Zero+HAT；头 IMU = HAT BMI088；机身 IMU = **测试 1 号 / 2 号二选一上机**。

## 装机结论

| # | 定论 |
|---|------|
| 1 | [[radxa-zero-3w]] + [[board-hat]] **叠装在头部** |
| 2 | 头 IMU = HAT **BMI088**（不另做专板） |
| 3 | 机身 IMU 见 [[board-imu-to-dxl]]：**1 号 32×22（优先）** · 2 号暂缓 |

## 现行板表

| 板 | 信息卡 | 角色 | 外形 / 固定 | 状态 |
|----|--------|------|-------------|------|
| **HAT** | [[board-hat]] | 电源 + DXL + 音频 + Qwiic + 头 BMI088 | 65×30.9 · 1.0 mm · 4L | 必装 · 头舱 |
| **主控** | [[radxa-zero-3w]] | RK3566 · 与 HAT 叠装 | 同 HAT | 必装 · 头舱 |
| **机身 IMU 1 号** | [[board-imu-to-dxl]] / [[imu-to-dxl-ref-bom]] | ID 200 · **v0.3** · 双 3P · BM07 | **32×22** · 四角 29×19 | **现行优先** |
| **机身 IMU 2 号** | [[board-imu-to-dxl]] | ID 200 · 简化 · **单 3P** | **22×15** · **两边中心 M2** | 测试打样 |

## 文档地图

| 需求 | 去哪 |
|------|------|
| 接线 / 装机 | [[board-interconnect]] |
| 1/2 号规格 | [[board-imu-to-dxl]] |
| 选型 | [[dual-imu-board-selection]] |
| DIY BOM | [[diy-bom]] |

相关：[[board-hat]] · [[board-imu-to-dxl]] · [[elec-rpi-robot-hat]] · [[imu-to-dxl-v2]]
