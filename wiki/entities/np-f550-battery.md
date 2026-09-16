---
title: NP-F550 电池
created: 2026-08-30
updated: 2026-09-11
type: entity
tags: [battery, power]
sources:
  - raw/articles/microduck-fact-sheet-2026.md
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/articles/taobao-np-f550-order-2026-09-11.md
confidence: high
related:
  - elec-rpi-robot-hat
  - board-interconnect
  - bench-power-supply
  - taobao-diy-procurement-2026-09
  - diy-bom
---

# NP-F550

可拆卸相机电池（索尼 L 系列外形）。Press Kit 写 2600 mAh；标称约 7.2–7.4 V；空约 6.6 V，负载满约 8.2 V（开路满电可 ~8.4 V）。经 [[elec-rpi-robot-hat]] 进电（电机口 `+BATT`/`GND`）；电量由舵机母线电压推断。alpha 网格占位名 `np_f970`（实为 F550 包络）。

无电池台架供电见 [[bench-power-supply]]。

## DIY 采购（2026-09-11）

| 项 | 值 |
|----|-----|
| 订单 | `3316416782030002460` · fb数码旗舰店 · ¥90 |
| 套装 | 沣标 **NP-F550 2200 mAh ×2** + **标准双充** |
| 链接 | https://item.taobao.com/item.htm?id=585415365001 |
| 归档 | `assets/procurement/taobao-np-f550-order-2026-09-11.xlsx` · [[taobao-diy-procurement-2026-09]] |

### 组装计划

组装时：**拆下一个充电器的充电头（触点板）**，固定到打印件 **`power_support`** 上，作机身电池取电；导线再接 HAT `+BATT`/`GND`。另一充电器保留外充。

相关：[[board-interconnect]] · [[microduck]] · [[elec-rpi-robot-hat]] · [[diy-bom]]
