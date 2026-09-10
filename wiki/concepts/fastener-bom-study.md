---
title: 紧固件研究 BOM
created: 2026-09-01
updated: 2026-09-03
type: concept
tags: [mechanical, fastener, bom]
sources:
  - raw/transcripts/research-hardware-servos-2026-08.md
  - https://www.robotis.us/dynamixel-xl330-m288-t/
confidence: medium
related: [mechanical-bom-rl, print-bom-rl, diy-bom, dynamixel-xl330]
---

# 紧固件研究 BOM

**非官方装箱单。** 摘自研究模型 `FASTENER_BOM.csv` + 孔位反推；舵机钉规格以 ROBOTIS 装箱为准。

## 示意级明细

| 分总成 | 规格 | 数量 | 长度 | 状态 |
|--------|------|------|------|------|
| 机身壳 | M2 内六角/圆头 | 6 | 6–8 mm | 研究假设 |
| 头壳 | M2 | 4 | 6–8 mm | 假设 |
| 电池门 | M2 | 2 | 6 mm | 假设 |
| 脚 | M2 | 4 | 8 mm | 假设 |
| **示意小计** | M2 | **16** | — | ≠ 官方真实数 |
| 打印凸台 | M2 热熔铜螺母 | 12 | 3–4 mm | 原型建议 |
| 定位 | Ø2 mm 销 | 6 | TBD | 原型建议 |
| 舵机法兰（horn） | **PHS M2×6 TAP** | **6**/台 | 6 mm | 官方装箱 |
| 舵机→框架 | **PHS M2×8 TAP** | **10**/台 | 8 mm | 官方装箱 |
| 金属 horn→框架 | PHS M2×4 | 6/套 | 4 mm | HNX330-N101 套装另配 |

## 长度分工（初样）

- M2×4：薄支架；金属 horn→frame  
- M2×6：壳、门、薄电子支架；**horn 固定（官方 TAP）**  
- M2×8：脚、带嵌件厚位；**机身→框架（官方 TAP）**  
- M2×10/12：仅双层穿过  
- M2.5×4：Pi 类孔（量产 [[radxa-zero-3w]] 另核）

## 整机粗估

以 **M2** 为主；约 **110–160** 颗（含舵机原厂钉）。15 台舵机自带：horn 钉 **90** + frame 钉 **150**。Dev Pack 配比未公开。

相关：[[mechanical-bom-rl]] · [[diy-bom]] · [[dynamixel-xl330]] · [[opensource-coverage]]
