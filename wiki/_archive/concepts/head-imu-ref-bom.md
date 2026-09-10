---
title: 头部 IMU 参考板 BOM
created: 2026-09-04
updated: 2026-09-05
type: concept
tags: [imu, board, bom, jlceda]
sources:
  - concepts/head-imu-ref-schematic.md
  - concepts/dual-imu-board-selection.md
confidence: medium
related:
  - head-imu-ref-schematic
  - dual-imu-board-selection
  - imu-to-dxl-ref-bom
  - elec-rpi-robot-hat
  - diy-bom
  - elec-three-board-bom
  - head-imu-lcsc-order-2026-09-05
  - vl53-tof
---

# 头部 IMU 参考板 BOM（板 B）

> **REFERENCE — NOT OFFICIAL。** 来自 HD `head_imu_ref` / `imu_head`（[[head-imu-ref-schematic]]）。  
> **控制环不用**；只认机身 [[imu-to-dxl-v2]]。与 HAT STEMMA QT / ToF 同 I²C 域。  
> **采购：** 立创 `SO26090520046` + U1 他渠 → [[head-imu-lcsc-order-2026-09-05]]。

| 项 | 值 |
|----|-----|
| 板名 | 头内 6 轴 I²C 模块 |
| 数量 | **1** / 整机（基础功能可后置） |
| 板框 | **18×14 mm** · 厚 0.8–1.0 mm |
| 必贴 | **5** |
| DNP | **2**（R1、R2 上拉） |

## 明细

| Ref | 型号 | LCSC | Qty | 封装 | 贴装 | 说明 |
|-----|------|------|-----|------|------|------|
| U1 | LSM6DSV16XTR | C5267406 | 1 | LGA-14 | 必贴 | **I²C**；CS→+3V3；SA0→GND → **0x6A** |
| J1 | BM04B-SRSS-TB | C160390 | 1 | SH 1.0 4P 立式 | 必贴 | STEMMA QT：1=GND 2=+3V3 3=SDA 4=SCL |
| C1 | 100 nF | C1525 | 1 | 0402 | 必贴 | Vdd 去耦 |
| C2 | 100 nF | C1525 | 1 | 0402 | 必贴 | Vdd_IO 去耦 |
| C3 | 1 µF | C52923 | 1 | 0402 | 必贴 | 入口 bulk · 近 J1 |
| R1 | 10 kΩ | C25744 | 1 | 0402 | **DNP** | SCL 上拉（网表接 SCL；HAT 已有则不焊） |
| R2 | 10 kΩ | C25744 | 1 | 0402 | **DNP** | SDA 上拉 |
| R3 | 0 Ω 或 10 k | — | 1 | 0402 | 可选 | SA0 选址；默认硬接 GND |
| TP1 | 测试点 | — | 1 | — | 可选 | INT1 |
| TP2/3 | 测试点 | — | 2 | — | 可选 | SDA / SCL |

可选说明：若需引出 INT，可改 **BM05B-SRSS-TB**（C160391）pin5=`IMU_INT`（定稿默认仍为 4P）。

## 采购合并

| LCSC | 型号/值 | 单板 | 备注 |
|------|---------|------|------|
| C5267406 | LSM6DSV16XTR | 1 | 与机身同料 |
| C160390 | BM04B-SRSS-TB | 1 | |
| C1525 | 100 nF 0402 | **2** | C1–C2 |
| C52923 | 1 µF 0402 | 1 | |
| C25744 | 10 kΩ 0402 | 2 | DNP；与 HAT/机身合并，可不买 |

备选传感器（供货压力）：LSM6DSOX / BMI088 — 非首选。

## 采购实绩（2026-09-05）

| 渠道 | 内容 | 记录 |
|------|------|------|
| 立创 `SO26090520046` | 4 行被动+座 · ¥16.59 | [[head-imu-lcsc-order-2026-09-05]] |
| 淘宝 | U1 LSM6（共用 ×6 池 · 09-05） | [[taobao-diy-procurement-2026-09]] |
| 立创配单 | `BOM260905003290` · 5 套报价 ¥127.23 | `assets/procurement/imu-head-ref-BOM-lcsc-20260905.xls` |

相关：[[head-imu-ref-schematic]] · [[head-imu-lcsc-order-2026-09-05]] · [[taobao-diy-procurement-2026-09]] · [[diy-bom]] · [[elec-rpi-robot-hat]]
