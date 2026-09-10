---
title: 台架供电（无电池）
created: 2026-08-30
updated: 2026-08-30
type: concept
tags: [power]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: high
---

# 台架供电（无电池）

| 场景 | 供电 |
|------|------|
| 仅 [[radxa-zero-3w]] | **5V Type-C**；推荐 Radxa **PD30W** 或 ≥5V/2A（≥15W）优质头 |
| HAT + 舵机 | **勿指望 USB-C**；向 [[elec-rpi-robot-hat]] 电池口供 **7.4–8.4 V**，建议 **5–10 A** 台供 |

整机正常路径：[[np-f550-battery]] → HAT → 5V 给 Radxa。双供电冲突需小心。

相关：[[board-interconnect]] · [[radxa]] · [[dynamixel-xl330]]
