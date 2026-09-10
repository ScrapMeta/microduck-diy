---
title: replica 机身 IMU 立创采购 · SO2609080348 + Y38
created: 2026-09-08
updated: 2026-09-08
type: concept
tags: [imu, board, bom, procurement, replica]
sources:
  - raw/articles/lcsc-imu-to-dxl-replica-bom-order-so2609080348-2026-09-08.md
  - raw/articles/jlcpcb-imu-to-dxl-replica-y38-2026-09-08.md
  - raw/articles/taobao-diy-orders-2026-08-09.md
confidence: high
related:
  - imu-to-dxl-replica-bom
  - board-imu-to-dxl-replica
  - imu-to-dxl-ref-bom
  - imu-to-dxl-lcsc-order-2026-09-05
  - board-imu-to-dxl
  - diy-bom
  - taobao-diy-procurement-2026-09
---

# replica 机身 IMU 立创采购（到货核对）

> 本页只留**订单状态与指针**；**完整 BOM（含每行采购）**见 [[imu-to-dxl-replica-bom]]。  
> 信息卡：[[board-imu-to-dxl-replica]]。对照：[[imu-to-dxl-ref-bom]]。

| 项 | 值 |
|----|-----|
| 板 | [[board-imu-to-dxl-replica]] · 非 HD `imu_to_dxl_ref` |
| BOM 配单 | `BOM260908000145`（报价 **5 套** · ¥225.86） |
| 元器件单 | **`SO2609080348`** · 2026-09-08 00:49 · ¥84.23 |
| PCB 制板 | **`Y38`** · 2026-09-08 00:48:07 · ⏳ |
| 元器件状态 | **⏳ 立创待收** · MCU/IMU 由淘宝共用池覆盖 → [[taobao-diy-procurement-2026-09]] |

## PCB 制板 · Y38

| 项 | 值 |
|----|-----|
| 工程名 | `imu_to_dxl_PCB1_20260908_004528` |
| 规格 | **双面板** · **5 片** · 绿色 · **无铅 OSP** |
| 交期 | 正常 **3 天** |
| 到货 | ⏳ |
| 摘要 | `raw/articles/jlcpcb-imu-to-dxl-replica-y38-2026-09-08.md`（口述入库，无导出文件） |

## 原件（元器件）

| 文件 | 路径 |
|------|------|
| BOM / 订单 XLS | `assets/procurement/imu-to-dxl-replica-BOM-lcsc-20260908.xls` · `lcsc-order-SO2609080348-20260908.xls` |
| 摘要（勾选行） | `raw/articles/lcsc-imu-to-dxl-replica-bom-order-so2609080348-2026-09-08.md` |

## 渠道拆分

| 渠道 | 内容 |
|------|------|
| **立创 PCB `Y38`** | 空板 ×5 · 双面绿 OSP · 正常 3 天 |
| **立创元器件 `SO2609080348`** | 无源、TVS、稳压管、PTC、双 EH、6P 排针、HT7533、**SN74LVC2G241** · **13 行** |
| **淘宝共用** | U1 [STM32G031](https://item.taobao.com/item.htm?id=726808419708) · U2 [LSM6DSV16X](https://item.taobao.com/item.htm?id=1028742717053)（与 ref/头同池） |

## 到货勾选（13）

| # | LCSC | 型号 | 位号 | 订购 | 到货 |
|---|------|------|------|------|------|
| 1 | C19702 | 10µF/10V 0603 | C7 | 20 | ⏳ |
| 2 | C19666 | 4.7µF/16V 0603 | C5 | 10 | ⏳ |
| 3 | C15850 | 10µF/25V 0805 | C6 | 20 | ⏳ |
| 4 | C14663 | 100nF 0603 | C1–C4,C8 | 50 | ⏳ |
| 5 | C2943870 | SMF12A | D1 | 20 | ⏳ |
| 6 | C160259 | B3B-EH-A | J1+J2 | 20 | ⏳ |
| 7 | C25804 | 10kΩ 0603 | R1,R2,R4,R5 | 100 | ⏳ |
| 8 | C22808 | 150Ω 0603 | R6 | 100 | ⏳ |
| 9 | C210358 | MF-NSMF020X-2 | F1 | 10 | ⏳ |
| 10 | C492405 | PZ254V 6P | J3 | 20 | ⏳ |
| 11 | C14289 | HT7533-1 | U4 | 5 | ⏳ |
| 12 | C151588 | BZT52C5V1 | D2 | 10 | ⏳ |
| 13 | C10430 | SN74LVC2G241 | U3 | 5 | ⏳ |

相关：[[imu-to-dxl-replica-bom]] · [[imu-to-dxl-ref-bom]] · [[diy-bom]] · [[taobao-diy-procurement-2026-09]] · [[board-imu-to-dxl]]
