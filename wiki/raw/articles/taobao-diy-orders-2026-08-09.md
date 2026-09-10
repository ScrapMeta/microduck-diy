---
source_url: null
ingested: 2026-09-08
sha256: b8d4aca639a5fafe9c32309ba9a659453dda5a5f6d005d8bacea40e188e67720
note: Taobao export 近一月订单; PII none in sheet; links stripped to item.htm?id=; binaries wiki/assets/procurement/taobao-orders-2026-08-09.xlsx
---

# 淘宝近一月订单 · DIY 相关摘录

> Source: `订单数据 (1).xlsx` → `wiki/assets/procurement/taobao-orders-2026-08-09.xlsx`  
> 仅摘与 Microduck DIY / 三板 BOM / 机械相关行；餐饮等无关项省略。  
> 商品链接已去 `mi_id` 追踪参数。状态以导出时为准。

## A. 三板关键 IC / 连接器（2026-09-05 同批补货）

母单时间均为 **2026-09-05 19:32** · 状态多为「卖家已发货」。

| 淘宝订单尾号 | 店铺 | 型号 / 规格 | 数量 | 单价 | 对应 BOM | 链接 |
|--------------|------|-------------|------|------|----------|------|
| …002460 | 深圳市新纶电子 | STM32G031F8P6 | 5 | ¥4.88 | 机身 ref U2 · replica U1 | https://item.taobao.com/item.htm?id=726808419708 |
| …002460 | 同上 | LSM6DSV16XTR | 6 | ¥16.80 | 机身 ref U1 · 头 U1 · replica U2 | https://item.taobao.com/item.htm?id=1028742717053 |
| …002460 | 同上 | BMI088 | 1 | ¥22.18 | HAT U11 | https://item.taobao.com/item.htm?id=766282759999 |
| …002460 | 同上 | LM5050MKX-1/NOPB | 5 | ¥2.65 | HAT U10 | https://item.taobao.com/item.htm?id=839365407611 |
| …002460 | 同上 | TLV320AIC3104IRHBR | 5 | ¥5.88 | HAT U2 | https://item.taobao.com/item.htm?id=739806672835 |
| …093661 | 欧贝顿旗舰店 | 0402 150Ω 1%（100 只） | 1 包 | ¥2.00 | HAT R33 | https://item.taobao.com/item.htm?id=608845773412 |
| …120489 | 深圳锋联芯 | 2059-302/998-403 | 15 | ¥0.90 | HAT J1,J2,J9 | https://item.taobao.com/item.htm?id=839082512633 |
| …139670 | 开立方芯商城 | BM04B-SRSS-TB | 30 | ¥0.60 | HAT J5–J8 · 机身/头 SWD | https://item.taobao.com/item.htm?id=856047296719 |
| …148852 | 博睿玛电子 | SIT3088EEUA | 5 | ¥1.46 | HAT U8 | https://item.taobao.com/item.htm?id=743572985338 |
| …166498 | 金芯辉电子 | LMA2718T421-OA5-2 | 5 | ¥0.68 | HAT MK1 | https://item.taobao.com/item.htm?id=954383582663 |
| …175680 | 立嘉诚电子 | 2.54-4P TPGT | 5 | ¥1.20 | HAT H2 | https://item.taobao.com/item.htm?id=892915491363 |
| …184862 | 原芯商城 3号店 | FH-00339 2×20P | 5 | ¥3.50 | HAT J4 | https://item.taobao.com/item.htm?id=1042574635268 |

新纶单实付合计约 **¥190.01**（含上表 5 行 IC）。

## B. 线材 / 主控 / 相机 / 舵机 / 轴承 / 紧固件（摘要）

| 日期 | 状态 | 商品 | 数量 | 对应 | 链接 |
|------|------|------|------|------|------|
| 09-03 | 已发货 | EH2.5 3P 双头线 0.1/0.2/0.3 m | 1+5+1 | DXL 总线线 [[board-interconnect]] | https://item.taobao.com/item.htm?id=972585639310 |
| 09-01 | 已发货 | Pi Camera Module V2 | 1 | 相机（官方 Camera V2 / IMX219 路径） | https://item.taobao.com/item.htm?id=921313362410 |
| 08-31 | 已发货 | 轴承 16×22×4 | 1 | [[seeed-bearings]] 大轴承 | https://item.taobao.com/item.htm?id=930534977802 |
| 08-31 | 已发货 | 轴承 10×15×3 | 3 | [[seeed-bearings]] 小轴承 | 同上 |
| 08-29 | 已发货 | 轴承 16×22×4 | 10 | 大轴承补齐至 **11** | 同上 |
| 08-29 | 已发货 | RADXA ZERO 3W 2G+0G | 1 | [[radxa-zero-3w]] | https://item.taobao.com/item.htm?id=746425059858 |
| 08-29 | 已发货 | XL330-M288-T-CN + 启动套件(国产) | 1+1 | [[dynamixel-xl330]]（淘宝样机；主批量仍 ROBOTIS） | https://item.taobao.com/item.htm?id=638117456346 |
| 08-29 | 交易关闭 | 同上 / Camera V2 另店 | — | **无效** | — |
| 08-29 | 成功 | XT30↔Type-C 线 | 1m+0.5m | [[bench-power-supply]] | https://item.taobao.com/item.htm?id=1060029647292 |
| 08-15 | 成功 | IMX415 30P 无畸变 120° | 1 | 非网格默认 IMX219；实验相机 | https://item.taobao.com/item.htm?id=725478193843 |
| 09-04/03/01 | 已发货 | M2 机牙/自攻/薄头/热熔铜螺母 多规格 | 多包 | [[fastener-bom-study]] / [[diy-bom]] §D | 金超等（见原表） |

## C. 与立创缺口对照（电子）

立创 HAT `SO26090519869` 曾列 10 项未订 → **本批淘宝已全部覆盖**（BMI088 仅 ×1，其余按 5 套量）。  
机身/头/replica 缺的 STM32 + LSM6 → **本批已购**（MCU×5 · IMU×6）。
