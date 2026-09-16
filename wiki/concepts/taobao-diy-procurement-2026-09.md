---
title: 淘宝 DIY 采购对照（2026-08～09）
created: 2026-09-08
updated: 2026-09-11
type: concept
tags: [procurement, bom, taobao]
sources:
  - raw/articles/taobao-diy-orders-2026-08-09.md
  - raw/articles/taobao-np-f550-order-2026-09-11.md
confidence: high
related:
  - diy-bom
  - np-f550-battery
  - elec-hat-lcsc-order-2026-09-05
  - imu-to-dxl-lcsc-order-2026-09-05
  - head-imu-lcsc-order-2026-09-05
  - imu-to-dxl-replica-lcsc-order-2026-09-08
  - board-imu-to-dxl-replica
  - elec-three-board-bom
---

# 淘宝 DIY 采购对照（近一月）

> 原件：`assets/procurement/taobao-orders-2026-08-09.xlsx`  
> 脱敏摘要：`raw/articles/taobao-diy-orders-2026-08-09.md`  
> 本页把相关行**挂回各 BOM**；链接为 `item.htm?id=` 干净链。

## 三板电子 · 已补齐（相对立创缺口）

| BOM | Ref | 型号 | 淘宝数量 | 单价 | 店铺/日期 | 链接 |
|-----|-----|------|----------|------|-----------|------|
| [[elec-rpi-robot-hat]] | U11 | BMI088 | 1 | ¥22.18 | 新纶 · 09-05 | [商品](https://item.taobao.com/item.htm?id=766282759999) |
| HAT | U2 | TLV320AIC3104IRHBR | 5 | ¥5.88 | 同上 | [商品](https://item.taobao.com/item.htm?id=739806672835) |
| HAT | U8 | SIT3088EEUA | 5 | ¥1.46 | 博睿玛 · 09-05 | [商品](https://item.taobao.com/item.htm?id=743572985338) |
| HAT | U10 | LM5050MKX-1/NOPB | 5 | ¥2.65 | 新纶 · 09-05 | [商品](https://item.taobao.com/item.htm?id=839365407611) |
| HAT | J1/J2/J9 | 2059-302/998-403 | 15 | ¥0.90 | 锋联芯 · 09-05 | [商品](https://item.taobao.com/item.htm?id=839082512633) |
| HAT | J4 | FH-00339 | 5 | ¥3.50 | 原芯 · 09-05 | [商品](https://item.taobao.com/item.htm?id=1042574635268) |
| HAT | J5–J8 等 | BM04B-SRSS-TB | 30 | ¥0.60 | 开立方 · 09-05 | [商品](https://item.taobao.com/item.htm?id=856047296719) |
| HAT | H2 | 2.54-4P TPGT | 5 | ¥1.20 | 立嘉诚 · 09-05 | [商品](https://item.taobao.com/item.htm?id=892915491363) |
| HAT | MK1 | LMA2718T421-OA5-2 | 5 | ¥0.68 | 金芯辉 · 09-05 | [商品](https://item.taobao.com/item.htm?id=954383582663) |
| HAT | R33 | 0402 150Ω | 100 | ¥2.00/包 | 欧贝顿 · 09-05 | [商品](https://item.taobao.com/item.htm?id=608845773412) |
| [[imu-to-dxl-ref-bom]] | MCU | STM32G031F8P6 | 5 | ¥4.88 | 新纶 · 09-05 | [商品](https://item.taobao.com/item.htm?id=726808419708) |
| 机身 IMU | IMU | LSM6DSV16XTR | 6 | ¥16.80 | 同上 | [商品](https://item.taobao.com/item.htm?id=1028742717053) |

BM04B ×30 同时覆盖 HAT×4 + 机身 SWD + 头 SWD（与立创已订座可合并库存）。

## 整机其它（挂 [[diy-bom]]）

| 分类 | 内容 | 状态 | 链接 |
|------|------|------|------|
| 主控 | RADXA ZERO 3W 2G | 08-29 已发货 · ¥472 | [商品](https://item.taobao.com/item.htm?id=746425059858) |
| 轴承 | 16×22×4 ×(10+1)=**11**；10×15×3 ×**3** | 已发货 | [商品](https://item.taobao.com/item.htm?id=930534977802) |
| 舵机 | XL330-M288-T-CN + 国产启动套件 | 08-29 已发货（样机；主批仍 [[robotis-xl330-order-2026-09-05]]） | [商品](https://item.taobao.com/item.htm?id=638117456346) |
| 相机 | Pi Camera V2 | 09-01 已发货 | [商品](https://item.taobao.com/item.htm?id=921313362410) |
| 相机(试验) | IMX415 30P | 08-15 成功 | [商品](https://item.taobao.com/item.htm?id=725478193843) |
| 线材 | EH 3P 双头 · XT30↔Type-C | 已购 | EH [商品](https://item.taobao.com/item.htm?id=972585639310) · XT30 [商品](https://item.taobao.com/item.htm?id=1060029647292) |
| 紧固件 | M2 多规格 + 热熔铜螺母 | 09-01～04 多单 | 见 raw / [[fastener-bom-study]] |
| **电池** | 沣标 **NP-F550 2200 mAh ×2 + 标准双充** | **09-11 已付款 · ¥90** · [[np-f550-battery]] | [商品](https://item.taobao.com/item.htm?id=585415365001) |

### 电池组装备注（09-11）

- 订单 `3316416782030002460` · 归档 `assets/procurement/taobao-np-f550-order-2026-09-11.xlsx` · 摘要 `raw/articles/taobao-np-f550-order-2026-09-11.md`
- **计划：** 拆下一个充电器的充电头，装到 **`power_support`** 作取电触点；另一充电器外充。

## 仍注意

- BMI088 **只买了 1 颗**（非 5 套）；首板够用。  
- 淘宝 XL330 为样机/套件，**15 台主单仍是 ROBOTIS**。  
- 交易关闭单（另店 Camera / 智能佳重复单）**不计库存**。

相关：[[diy-bom]] · [[elec-hat-lcsc-order-2026-09-05]] · [[imu-to-dxl-lcsc-order-2026-09-05]] · [[imu-to-dxl-lcsc-order-2026-09-09]]
