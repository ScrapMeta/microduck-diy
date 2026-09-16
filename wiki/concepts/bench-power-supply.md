---
title: 台架供电（无电池）
created: 2026-08-30
updated: 2026-09-16
type: concept
tags: [power]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: high
---

# 台架供电（无电池）

| 场景 | 供电 |
|------|------|
| 仅 [[radxa-zero-3w]] | **5V Type-C**；推荐 Radxa **PD30W** 或 ≥5V/2A（≥15W）优质头 |
| HAT + 舵机 | **勿指望 USB-C**；向 [[elec-rpi-robot-hat]] 电池口供 **6.0–6.5 V**，台供 **≥3 A** |

**电压口径已收口（2026-09-16）**：本页原写「7.4–8.4 V」，那是照 NP-F 标称写的。实测这批 XL330 **~7.2 V 即过压报警**（手册上限 6.0 V，Max Voltage Limit ≈7.0 V），
且 `shutdown=52` 会**锁存 input-voltage fault 并保持 torque off**。**台架一律 6.0–6.5 V。**

整机正常路径：[[np-f550-battery]] → HAT → 5V 给 Radxa。**NP-F 直供（6.6–8.4 V）会超舵机上限**，DIY 建议机身加 buck 降到 **6.0–6.5 V** 再粗线进 HAT，
见 [[body-imu-hat-dxl-power-eval]] §3.1/§5（整机行走峰值预算 **数安以上**，故整机台供按 5–10 A 备）。双供电冲突需小心。

相关：[[board-interconnect]] · [[radxa]] · [[dynamixel-xl330]] · [[body-imu-hat-dxl-power-eval]]
