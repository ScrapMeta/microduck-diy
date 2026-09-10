---
title: Feetech STS3032
created: 2026-08-30
updated: 2026-08-30
type: entity
tags: [servo, feetech]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: medium
---

# Feetech STS3032

飞特里**最贴近** [[dynamixel-xl330]] 电气档的候选：约 4.8–6 V，堵转 ~4.5 kg·cm @6 V，~20 g，磁编 4096，STS TTL。外形多为 **12 mm 细长壳**，非 XL 20×34 安装。

## 注意

- 协议飞特 STS，非 DXL 2.0 → 不能直接跑 `robotd`
- [[better-actuator-models-bam]] **无**现成模型，需自辨识
- 舵盘 25T，机械要改

相关：[[feetech]] · [[xl330-vs-feetech-servos]] · [[better-actuator-models-bam]]
