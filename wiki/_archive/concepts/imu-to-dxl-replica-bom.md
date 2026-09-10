---
title: imu_to_dxl replica 完整 BOM（含采购）
created: 2026-09-08
updated: 2026-09-08
type: concept
tags: [imu, board, bom, replica, procurement]
sources:
  - raw/articles/lcsc-imu-to-dxl-replica-bom-order-so2609080348-2026-09-08.md
  - raw/articles/jlcpcb-imu-to-dxl-replica-y38-2026-09-08.md
  - raw/articles/taobao-diy-orders-2026-08-09.md
confidence: high
related:
  - board-imu-to-dxl-replica
  - imu-to-dxl-replica-lcsc-order-2026-09-08
  - imu-to-dxl-ref-bom
  - board-imu-to-dxl
  - diy-bom
  - taobao-diy-procurement-2026-09
---

# imu_to_dxl replica 完整 BOM（含采购）

> **COMMUNITY** · 信息卡 [[board-imu-to-dxl-replica]]。  
> 配单 `BOM260908000145` · `imu_to_dxl_PCB1_20260908_004024`。  
> 订单指针：[[imu-to-dxl-replica-lcsc-order-2026-09-08]] · 淘宝总表 [[taobao-diy-procurement-2026-09]]。  
> **单板 qty** 如下；立创/淘宝按 **5 套** 量下单处已注明。

## PCB

| 项 | 规格 | 数量 | 渠道 | 订单 | 状态 |
|----|------|------|------|------|------|
| 空板 | 双面 · 绿 · 无铅 OSP · `imu_to_dxl_PCB1_20260908_004528` | 5 | 立创 PCB | **Y38** · 09-08 00:48 | ⏳ |

## 完整料表（16 行 + 采购）

| Ref | 型号 / 值 | LCSC | 单板 | 渠道 | 订单/池 | 链接 |
|-----|-----------|------|------|------|---------|------|
| U1 | STM32G031F8P6 | C529334 | 1 | 淘宝 | 新纶 ×5 · 09-05 | [淘宝](https://item.taobao.com/item.htm?id=726808419708) |
| U2 | LSM6DSV16XTR | C5267406 | 1 | 淘宝 | 新纶 ×6 · 09-05（与 ref/头共用） | [淘宝](https://item.taobao.com/item.htm?id=1028742717053) |
| U3 | SN74LVC2G241DCUR | C10430 | 1 | 立创 | `SO2609080348` ×5 | [立创](https://item.szlcsc.com/10973.html) |
| U4 | HT7533-1 | C14289 | 1 | 立创 | 同上 ×5 | [立创](https://item.szlcsc.com/14949.html) |
| D1 | SMF12A | C2943870 | 1 | 立创 | 同上 ×20 | [立创](https://item.szlcsc.com/3328926.html) |
| D2 | BZT52C5V1-7-F | C151588 | 1 | 立创 | 同上 ×10 | [立创](https://item.szlcsc.com/162928.html) |
| F1 | MF-NSMF020X-2 | C210358 | 1 | 立创 | 同上 ×10 | [立创](https://item.szlcsc.com/211705.html) |
| J1 | B3B-EH-A | C160259 | 1 | 立创 | 同上（J1+J2 共 ×20） | [立创](https://item.szlcsc.com/171639.html) |
| J2 | B3B-EH-A | C160259 | 1 | 立创 | 同上 | 同上 |
| J3 | PZ254V-11-06P | C492405 | 1 | 立创 | 同上 ×20 | [立创](https://item.szlcsc.com/502961.html) |
| C1–C4,C8 | 100 nF 0603 | C14663 | 5 | 立创 | 同上 ×50 | [立创](https://item.szlcsc.com/15331.html) |
| C5 | 4.7 µF/16V 0603 | C19666 | 1 | 立创 | 同上 ×10 | [立创](https://item.szlcsc.com/20375.html) |
| C6 | 10 µF/25V 0805 | C15850 | 1 | 立创 | 同上 ×20 | [立创](https://item.szlcsc.com/16532.html) |
| C7 | 10 µF/10V 0603 | C19702 | 1 | 立创 | 同上 ×20 | [立创](https://item.szlcsc.com/20411.html) |
| R1,R2,R4,R5 | 10 kΩ 0603 | C25804 | 4 | 立创 | 同上 ×100 | [立创](https://item.szlcsc.com/26547.html) |
| R6 | 150 Ω 0603 | C22808 | 1 | 立创 | 同上 ×100 | [立创](https://item.szlcsc.com/23535.html) |

**覆盖：** 设计 16 行全部有采购渠道；无「未订」行。立创实付 ¥84.23（13 行）；MCU/IMU 在淘宝共用池。

## vs 本仓 ref

| 维度 | replica（本页） | [[imu-to-dxl-ref-bom]] |
|------|-----------------|------------------------|
| PHY | 2G241 | 1G125 |
| LDO | HT7533-1 | AP2210K |
| 座 | 双 EH + 6P | EH + BM04 SWD |
| 位号 | U1=MCU · U2=IMU | 对调 |

## 原件

| 文件 | 路径 |
|------|------|
| BOM / 料单 XLS | `assets/procurement/imu-to-dxl-replica-BOM-lcsc-20260908.xls` · `lcsc-order-SO2609080348-20260908.xls` |
| 摘要 | `raw/articles/lcsc-imu-to-dxl-replica-bom-order-so2609080348-2026-09-08.md` |

相关：[[board-imu-to-dxl-replica]] · [[imu-to-dxl-replica-lcsc-order-2026-09-08]] · [[taobao-diy-procurement-2026-09]] · [[board-imu-to-dxl]] · [[diy-bom]]
