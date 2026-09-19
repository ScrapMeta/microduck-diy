---
title: XL330 vs 飞特候选舵机
created: 2026-08-30
updated: 2026-09-19
type: comparison
tags: [comparison, servo, dynamixel, feetech]
sources:
  - raw/transcripts/research-hardware-servos-2026-08.md
  - raw/articles/openmicroduck-joyandai-2026-09-04.md
confidence: high
---

# XL330 vs 飞特候选舵机

比较对象：[[dynamixel-xl330]] 与 STS / HL / [[feetech-hd-1910]] / [[feetech-hl-2909]] 等。

| 维度 | XL330-M288 | HD-1910 | HL-2909† | STS3032 | STS3215 | HL-2915‡ | HL-3915 |
|------|------------|---------|----------|---------|---------|----------|---------|
| 电压 | 3.7–6 V | **4–8.4 V** | **9–14 V** | ~4.8–6 V | 4–7.4 V | ~9–14 V | 4–14 V |
| 堵转 | ~5.3 kg·cm | **15@7.4V / 12@6V** | **8.9** | ~4.5 | ~19 | 14.2‡ | 14.2 |
| 重量 | 18 g | **21 g** | 22.5 g | ~20 g | ~55 g 级 | ~28 g | ~36 g |
| 外形 | 20×34×26 | **20×34×26** | 20×34×23 | 细长 12 mm | 更大 | 20×34×23 | 20×34×23 |
| 协议 | DXL 2.0 | 飞特 TTL | 飞特 TTL | STS | STS | TTL/HLS | HLS |
| BAM | **有** | 无 | 无 | 无 | **有** | 无 | 无 |

† [[feetech-hl-2909]]：OpenMicroDuck 规格书（与 HL-2915-C002 同册）。  
‡ [[feetech-hl-2915]]：早期 wiki 口述口径，与规格书冲突时以 PDF 为准。

> **2026-09-19 订正**：HD-1910 那一列的电压 / 堵转 / 重量 / **外形**此前采自**预售期产品页**，
> 且与 HL-2915 互串——均已按飞特规格书 A/0（2026-09-07）更正为
> **4–8.4 V · 15 kg·cm@7.4V（12@6V）· 21 g · 20×34×26**（规格书的 23 mm 是**不含主舵盘**的量法，
> 含舵盘与 XL330 同尺寸）。现行页见 [[feetech-hd-1910]]，协议见 [[feetech-scs-bus]]。

## 结论

- 留在官方 Microduck 软件/结构：继续 XL330
- **飞特开源小鸭路线**：[[feetech-hd-1910]]（2S 友好）或 [[feetech-hl-2909]]（12 V，改供电更大）— 均见 [[openmicroduck]]
- 电气最贴且愿改壳：STS3032（仍要改协议）
- 愿做更大机 + 有 BAM：STS3215
- 要硬要力控：HL-3915；均非 drop-in，换机须重训

相关：[[hl2915-vs-hl3915]] · [[openmicroduck]] · [[better-actuator-models-bam]] · [[feetech]]
