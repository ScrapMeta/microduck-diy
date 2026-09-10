---
title: Seeed 轴承网格规格
created: 2026-09-01
updated: 2026-09-08
type: concept
tags: [mechanical, bom]
sources:
  - concepts/mechanical-bom-rl.md
  - raw/articles/taobao-diy-orders-2026-08-09.md
confidence: high
related: [mechanical-bom-rl, print-bom-rl, microduck-diy, diy-bom, taobao-diy-procurement-2026-09]
---

# Seeed 轴承网格规格

Onshape/MJCF 网格名含 Seeed 轴承族。尺寸由 STL 包络量得（mm）。

| 网格名 | RL 数量 | 内径×外径×厚 | 市售近似 | 采购 |
|--------|---------|--------------|----------|------|
| `seeed_bearing__configuration__22x16x4` | **11** | 16×22×4 | 薄壁深沟 | 淘宝已购 **11**（10+1） |
| `seeed_bearing__configuration_default` | **3** | 约 10×15×3 | 常见 **6700** 档 | 淘宝已购 **3** |
| `bearing_roll` | 2 | （滚道位网格） | 按实机另配 | 未订 |

链接：[轴承店](https://item.taobao.com/item.htm?id=930534977802) · 详见 [[taobao-diy-procurement-2026-09]]。

App alpha 曾为 default×2 + 大轴承×10；**以 RL 11+3 为准**。

## 实心占位（打印用）

去掉滚珠、滚道填实、保留端面倒角的垫片：

- `seeed_bearing__configuration_default_solid.stl`
- `seeed_bearing__configuration__22x16x4_solid.stl`

存放：工程侧实心占位 STL（装配预演用，非真轴承）。

相关：[[mechanical-bom-rl]] · [[diy-bom]] · [[taobao-diy-procurement-2026-09]] · [[microduck-diy]]
