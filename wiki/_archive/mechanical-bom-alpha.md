---
title: Alpha 机械 BOM（网格反推）
created: 2026-08-30
updated: 2026-09-06
type: concept
tags: [mechanical, bom, fastener]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: medium
related: [mechanical-bom-rl, fastener-bom-study, print-bom-rl]
---

# Alpha 机械 BOM（网格反推）· 已归档

> **归档（2026-09-06）。** 打印/装配请用 [[mechanical-bom-rl]]。本页仅保留 alpha 网格历史对照。

来自 `microduck_app` alpha MJCF：`assets/*.stl`，**34 种 / 64 实例**。官方未公布机械装箱单。

## 高数量件（alpha）

- 15× `xl330`
- 10× seeed bearing 22×16×4；default 轴承 ×2
- 若干腿/髋/颈对称件 ×2

## 版本差

网格含 `pcb__raspberry_pi_zero_2_w`、`np_f970`；量产为 [[radxa-zero-3w]] + [[np-f550-battery]]。

## 紧固件

见 [[fastener-bom-study]]（原粗估：M2 为主，约 110–160 颗含舵机钉）。

相关：[[mechanical-bom-rl]] · [[dynamixel-xl330]] · [[opensource-coverage]]
