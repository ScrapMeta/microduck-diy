---
title: 机身 IMU 立创采购 · SO26090520116
created: 2026-09-05
updated: 2026-09-08
type: concept
tags: [imu, board, bom, procurement]
sources:
  - raw/articles/lcsc-imu-to-dxl-bom-order-so26090520116-2026-09-05.md
  - raw/articles/taobao-diy-orders-2026-08-09.md
confidence: high
related:
  - imu-to-dxl-ref-bom
  - board-imu-to-dxl
  - elec-three-board-bom
  - diy-bom
  - elec-hat-lcsc-order-2026-09-05
  - taobao-diy-procurement-2026-09
---

# 机身 IMU 立创采购（imu_to_dxl_ref · 到货核对）

> 本页只留**订单状态与指针**；设计料表见 [[imu-to-dxl-ref-bom]]。

| 项 | 值 |
|----|-----|
| 板 | [[board-imu-to-dxl]] · [[imu-to-dxl-ref-bom]] |
| BOM 配单 | `BOM260905003370`（报价 **5 套** · ¥205.01） |
| 立创 | **`SO26090520116`** · ¥54.40 |
| 淘宝 IC | STM32G031×5 · LSM6DSV16X×6（09-05 新纶）→ [[taobao-diy-procurement-2026-09]] |
| 状态 | **⏳ 立创+淘宝待收** |

## 原件

| 文件 | 路径 |
|------|------|
| BOM / 订单 XLS | `assets/procurement/imu-to-dxl-ref-BOM-lcsc-20260905.xls` · `lcsc-order-SO26090520116-20260905.xls` |
| 摘要（勾选行） | `raw/articles/lcsc-imu-to-dxl-bom-order-so26090520116-2026-09-05.md` |

## 渠道拆分

| 渠道 | 内容 |
|------|------|
| **立创本单** | 无源、TVS、LDO、缓冲、座、晶体等 **11 行** |
| **淘宝** | U1 [LSM6DSV16XTR](https://item.taobao.com/item.htm?id=1028742717053) ×6 · U2 [STM32G031F8P6](https://item.taobao.com/item.htm?id=726808419708) ×5（与头/replica 共用池；TP1 误配 FPC → **勿买**） |

相关：[[imu-to-dxl-ref-bom]] · [[taobao-diy-procurement-2026-09]] · [[diy-bom]] · [[elec-hat-lcsc-order-2026-09-05]]
