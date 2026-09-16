---
source_url: null
ingested: 2026-09-11
sha256: 64d8d1addec871833e2e2a6cd92b2fdecad49bddb34e2b0df52936a9bf9c6be
note: Taobao export 订单数据 (2).xlsx; NP-F550 2电+双充; assembly plan = harvest charger plate onto power_support
---

# 淘宝订单 · NP-F550 电池 + 充电器（2026-09-11）

> Source: `c:\Users\Intel\Downloads\订单数据 (2).xlsx`  
> 归档：`wiki/assets/procurement/taobao-np-f550-order-2026-09-11.xlsx`  
> 商品链接已去 `mi_id`。状态以导出时为准。

| 字段 | 值 |
|------|-----|
| 订单号 | `3316416782030002460` |
| 提交时间 | **2026-09-11 13:32:56** |
| 状态 | 买家已付款 |
| 店铺 | fb数码旗舰店 |
| 商品 | 沣标 NP-F550/F750 等补光灯电池（内置 Type-C 系列文案） |
| 型号款式 | **【NP-F550补光灯专用▲2200mAh】2电+标准双充套裝** |
| 数量 | 1（套） |
| 实付 | ¥90.00（运费 ¥0） |
| 链接 | https://item.taobao.com/item.htm?id=585415365001 |

## 组装计划（用户确认）

- 到货后：**拆下一个充电器的充电头（NP-F 触点板）**，装到 Microduck 打印件 **`power_support`（电池支撑板）** 上，作为机身取电触点。
- 用途：填补官方开源仓「只有 `power_support`、无触点模型」的空白（见 replica `BOM.md` §六）。
- 另一只充电器可作外充；两块 2200 mAh 兼容电轮换。
- ⚠️ 兼容电容量 **2200 mAh** ≠ Press Kit 文案 2600 mAh / 索尼原装常见 1500 mAh；外形按 **F550** 核对装机。
