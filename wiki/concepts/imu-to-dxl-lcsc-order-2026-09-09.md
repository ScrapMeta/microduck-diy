---
title: 机身 IMU 立创采购 · SO26090921960（v0.3）
created: 2026-09-09
updated: 2026-09-09
type: concept
tags: [imu, board, bom, procurement]
sources:
  - raw/articles/lcsc-imu-to-dxl-v03-bom-order-so26090921960-2026-09-09.md
confidence: high
related:
  - imu-to-dxl-ref-bom
  - board-imu-to-dxl
  - imu-to-dxl-lcsc-order-2026-09-05
  - diy-bom
  - imu-to-dxl-replica-bom
  - taobao-diy-procurement-2026-09
---

# 机身 IMU 立创采购（**v0.3** · `SO26090921960`）

> 设计料表：[[imu-to-dxl-ref-bom]]。旧单：[[imu-to-dxl-lcsc-order-2026-09-05]]。

| 项 | 值 |
|----|-----|
| 板 | [[board-imu-to-dxl]] · 丝印 **`imu-to-dxl v0.3`** |
| **v0.3 BOM 配单** | **`BOM260909006316`** · `imu_to_dxl_ref_…_PCB1_1_20260909_194740` · 报价 5 套 ¥195.02 |
| 立创订单 | **`SO26090921960`** · ¥112.58（商品 ¥105.69 + 运费 ¥8）· 2026-09-09 |
| 状态 | **⏳ 待收**（订单缺 BM07） |

## 原件

| 文件 | 路径 |
|------|------|
| **v0.3 BOM 报价** | `assets/procurement/imu-to-dxl-v03-BOM-lcsc-BOM260909006316-20260909.xls` |
| 订单 XLS | `assets/procurement/lcsc-order-SO26090921960-20260909.xls` |
| 摘要 | `raw/articles/lcsc-imu-to-dxl-v03-bom-order-so26090921960-2026-09-09.md` |
| 误传（replica） | `…BOM260909006112…` · 勿用 |

## BOM260909006316 行（设计对齐）

| 位号 | LCSC | 型号 | 单板 |
|------|------|------|------|
| U1 | C5267406 | LSM6DSV16XTR | 1 |
| U2 | C529334 | STM32G031F8P6 | 1 |
| U3 | C176959 | AP2210K-3.3 | 1 |
| U6 | C3040625 | SN74LVC1G125 | 1 |
| D1 | C2827694 | PESD5V0S1BA | 1 |
| D2 | C151348 | BZT52C5V1S-7-F | 1 |
| J1,J3 | C160259 | B3B-EH-A | 2 |
| J2 | **C160393**（配单匹配；需求曾写 C20089159） | **BM07B-SRSS-TB** | 1 |
| C1,C3 | C1525 | 100 nF | 2 |
| C4 | C307331 | 100 nF | 1 |
| C2 | C52923 | 1 µF | 1 |
| C5 | C440198 | 10 µF 50 V | 1 |
| C6 | C19666 | 4.7 µF | 1 |
| R1–R5 | C25744 | 10 kΩ | 5 |
| R6 | C22808 | 150 Ω | 1 |

无 Y1/C7/C8（DNP 未进配单）。J2 匹配状态为 **待确认**，未计入配单总价自动下单。

## 订单 `SO26090921960` vs 配单

核心 IC/电源/保护/无源/EH：**已订**（MCU×2、IMU×2）。  
**未订：BM07B J2**（配单有、订单无）→ 需另购 **C160393**（或确认等同料号）。

相关：[[imu-to-dxl-ref-bom]] · [[diy-bom]] · [[imu-to-dxl-lcsc-order-2026-09-05]]
