---
title: Dynamixel XL330
created: 2026-08-30
updated: 2026-09-06
type: entity
tags: [servo, dynamixel]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/transcripts/research-hardware-servos-2026-08.md
  - raw/articles/robotis-xl330-order-b260905014mp-2026-09-05.md
confidence: high
related: [elec-rpi-robot-hat, imu-to-dxl-v2, diy-bom, robotis-xl330-order-2026-09-05, robotis]
---

# Dynamixel XL330（M288-T）

Microduck **15 关节**执行器。典型 **XL330-M288-T**：20×34×26 mm，18 g，3.7–6 V，堵转约 0.52 N·m（~5.3 kg·cm）@5 V，塑料齿，Protocol **2.0** TTL。软件：`rustypot` / `Xl330Controller`。

## 项目内用法

- 总线经 [[elec-rpi-robot-hat]]；与 [[imu-to-dxl-v2]] 共线
- 产线写 ID/参数；现场一般不刷
- 仿真摩擦：[[better-actuator-models-bam]] 有 **XL330-288-T** 模型
- 实机母线常跟 [[np-f550-battery]]（约 6.6–8.2 V），高于官方 6 V 上限——按实机设计，注意过压风险

## DIY 采购

- 订单 **B260905014MP**（2026-09-05）：15× @ \$23.90 + DHL \$57.73 = **\$416.23** · Payment complete · ⏳待收  
- 详见 [[robotis-xl330-order-2026-09-05]] · 汇总入 [[diy-bom]] §C

相关：[[diy-bom]] · [[robotis-xl330-order-2026-09-05]] · [[robotis]]
