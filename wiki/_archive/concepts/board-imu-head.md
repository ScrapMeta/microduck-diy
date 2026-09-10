---
title: 头部 IMU 板信息卡（imu-head · 非必装）
created: 2026-09-05
updated: 2026-09-08
type: concept
tags: [board, imu, diy]
sources:
  - concepts/head-imu-ref-schematic.md
  - concepts/head-imu-ref-bom.md
confidence: medium
related:
  - elec-three-boards
  - board-interconnect
  - dual-imu-board-selection
  - head-imu-ref-schematic
  - head-imu-ref-bom
  - head-imu-lcsc-order-2026-09-05
  - board-hat
  - board-imu-to-dxl-replica
  - vl53-tof
---

# 头部 IMU 板信息卡（非必装）

> **REFERENCE — NOT OFFICIAL。**  
> **现行 DIY：头 IMU = [[board-hat]] 板载 BMI088**，本专板**不装机**（料作备件）。见 [[board-interconnect]] · [[dual-imu-board-selection]]。

## 1. 身份与角色

| 项 | 内容 |
|----|------|
| 丝印 | `imu-head v0.2` · huodianyan · `260905` |
| 工程建议名 | `head_imu_ref` / `imu_head` |
| DIY 地位 | **非必装**；控制环本来也不用头 IMU |
| 现行替代 | HAT **BMI088**（与主控同在头舱） |
| 总线 | **I²C** · 地址 **0x6A**（若仍组装本板） |
| IMU | **LSM6DSV16X**（CS 接 3V3 → I²C） |
| MCU | 无 |
| 供电 | 仅 **+3V3**（勿挂 VBATT） |

## 2. 外形与接口

| 项 | 值 | 备注 |
|----|-----|------|
| 板框 | **18×14 mm** | 定稿 |
| 厚度 | **0.8–1.0 mm** | 占位曾用 18×14×3 |
| 层数 | **未写入定稿** | 待下单参数补 |
| J1 | BM04B-SRSS-TB · STEMMA QT | GND / 3V3 / SDA / SCL |
| 上拉 | R1/R2 **DNP** | HAT 侧通常已有 |

## 3. CAD / 官方截图（wiki）

### v0.2 定稿（2026-09-05）

| 图 | 文件 |
|----|------|
| PCB 布线 | [`imu-head-v0.2-pcb-2026-09-05.png`](../assets/pcb/imu-head-v0.2-pcb-2026-09-05.png) |
| 3D 正面 | [`imu-head-v0.2-3d-2026-09-05.png`](../assets/pcb/imu-head-v0.2-3d-2026-09-05.png) |
| 摆放示意 | [`head-imu-placement.svg`](../assets/pcb/head-imu-placement.svg) |

![3D v0.2](../assets/pcb/imu-head-v0.2-3d-2026-09-05.png)

![PCB v0.2](../assets/pcb/imu-head-v0.2-pcb-2026-09-05.png)

### 历史 v0.1（2026-09-05）

| 图 | 文件 |
|----|------|
| 原理图 / PCB / 3D | `imu-head-v0.1-{sch,pcb,3d}-2026-09-05.png` |

## 4. 子文档地图

| 主题 | 页 |
|------|-----|
| 原理图 + 摆放全文 | [[head-imu-ref-schematic]] |
| 采购 BOM | [[head-imu-ref-bom]] |
| 立创实单 | [[head-imu-lcsc-order-2026-09-05]] |
| 选型 / 现行头 IMU | [[dual-imu-board-selection]] · [[board-hat]] |
| 接线 | [[board-interconnect]] |

## 5. 缺口（若仍组装）

| 缺什么 | 说明 |
|--------|------|
| v0.2 原理图截图 | 仅有 v0.1 sch PNG |
| 层数 | 未定稿写入 |

相关：[[elec-three-boards]] · [[board-hat]] · [[board-interconnect]] · [[dual-imu-board-selection]]
