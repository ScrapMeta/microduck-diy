---
title: Dynamixel XL330
created: 2026-08-30
updated: 2026-09-15
type: entity
tags: [servo, dynamixel]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/transcripts/research-hardware-servos-2026-08.md
  - raw/articles/robotis-xl330-order-b260905014mp-2026-09-05.md
  - raw/articles/xl330-cn-starter-kit-notes-2026-09-10.md
confidence: high
related: [elec-rpi-robot-hat, imu-to-dxl-v2, diy-bom, robotis-xl330-order-2026-09-05, xl330-cn-bench-kit, robotis, body-imu-hat-dxl-power-eval]
---

# Dynamixel XL330（M288-T）

Microduck **15 关节**执行器。典型 **XL330-M288-T**：20×34×26 mm，18 g，3.7–6 V，堵转约 0.52 N·m（~5.3 kg·cm）@5 V，塑料齿，Protocol **2.0** TTL。软件：`rustypot` / `Xl330Controller`。

规格书：[eManual XL330-M288](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)

## 项目内用法

- 总线经 [[elec-rpi-robot-hat]]；与 [[imu-to-dxl-v2]] 共线
- 产线写 ID/参数；现场一般不刷
- 仿真摩擦：[[better-actuator-models-bam]] 有 **XL330-288-T** 模型
- 实机母线：官方常跟 [[np-f550-battery]]（约 6.6–8.2 V），高于手册 6 V 上限。  
  **DIY 实测（2026-09-15）：** ~**7.2 V** 红灯持续闪（过压报警，默认 Max Voltage Limit≈7.0 V）；~**6.5 V** 上电闪一下后正常。装机建议母线 **6.0–6.5 V** 粗线进 HAT，见 [[body-imu-hat-dxl-power-eval]]。

## DIY 采购 / 台架

| 路径 | 说明 |
|------|------|
| Robotis 直邮 | 订单 **B260905014MP**：15× · [[robotis-xl330-order-2026-09-05]] |
| **CN 台架** | **XL330-M288-T-CN** + 国产 U2D2/PHB · [[xl330-cn-bench-kit]]（**✅ 通过** · 明细后补） |

相关：[[diy-bom]] · [[xl330-cn-bench-kit]] · [[robotis-xl330-order-2026-09-05]] · [[robotis]] · [[body-imu-hat-dxl-power-eval]]
