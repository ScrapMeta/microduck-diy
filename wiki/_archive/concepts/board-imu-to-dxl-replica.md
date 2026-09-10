---
title: 机身 IMU 板信息卡（replica · 机械不采用）
created: 2026-09-08
updated: 2026-09-09
type: concept
tags: [board, imu, diy, replica]
sources:
  - concepts/imu-to-dxl-replica-bom.md
  - raw/articles/microduck-replica-fanhao375-2026-09-01.md
confidence: high
related:
  - imu-to-dxl-replica-bom
  - imu-to-dxl-replica-lcsc-order-2026-09-08
  - board-imu-to-dxl
  - elec-three-boards
  - board-interconnect
  - diy-bom
  - taobao-diy-procurement-2026-09
---

# 机身 IMU 板信息卡（replica · 机械不采用）

> **COMMUNITY — fanhao375 `microduck-replica`。**  
> **2026-09-09 实测：板长与开孔均不合适 → DIY 装机不采用。**  
> 现行测试板：**1 号 32×22（优先）** → [[board-imu-to-dxl]]；2 号暂缓。
> 本页保留电气/BOM 对照与已下单料；勿再按 45×22 开孔抄机械。

## 0. 机械结论（用户实测）

| 项 | 结论 |
|----|------|
| 板长 **45 mm** | **不合适**（相对髋间/电池背板空间） |
| 开孔（对角 M2 · 宣称≈34 mm） | **不合适** |
| DIY 处置 | **不装机**；改打 [[board-imu-to-dxl]] 1/2 号 |

早期 wiki「借两髋孔、大小合适」作废。

## 1. 身份（电气对照仍可用）

| 项 | 内容 |
|----|------|
| 工程名 | `imu_to_dxl_PCB1`（立创 `…20260908_004528`） |
| 来源 | `microduck-replica` `hardware/imu_to_dxl` |
| 总线 | DXL 2.0 · ID **200** · addr **124** |
| IMU / MCU | LSM6DSV16X · STM32G031F8P6 |
| PHY | **SN74LVC2G241**（≠ 本仓 1G125 固件） |
| LDO | HT7533-1 |
| 设计外形 | **45×22** · 对角 2× M2 · 双 EH |

## 2. 采购（已发生）

| 项 | 指针 |
|----|------|
| 完整 BOM | [[imu-to-dxl-replica-bom]] |
| 立创 + 制板 Y38 | [[imu-to-dxl-replica-lcsc-order-2026-09-08]] |
| 淘宝 MCU/IMU | [[taobao-diy-procurement-2026-09]] |

空板/料可作电气实验；**不依赖其孔位装机**。

## 3. 相关

[[board-imu-to-dxl]] · [[elec-three-boards]] · [[board-interconnect]] · [[diy-bom]]
