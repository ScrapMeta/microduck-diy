---
title: Feetech HD-1910
created: 2026-09-08
updated: 2026-09-08
type: entity
tags: [servo, feetech]
sources:
  - raw/articles/openmicroduck-joyandai-2026-09-04.md
  - OpenMicroDuck/docs/servo.md
confidence: medium
related:
  - feetech
  - feetech-hl-2909
  - dynamixel-xl330
  - xl330-vs-feetech-servos
  - openmicroduck
---

# Feetech HD-1910（HD-1910M-C001 / HD-1910-C001）

飞特为「开源小鸭」路线预售的 **TTL 三针总线舵机**。相对 [[dynamixel-xl330]]：电压更贴 **2S（5–8.4 V）**，外形接近 XL 档但深度略浅；协议为飞特半双工，**不能**直接当 DXL 2.0 跑官方 `robotd`。

## 参数（公开页 + OpenMicroDuck 对照表）

| 项 | 值 |
|----|-----|
| 型号写法 | HD-1910M-C001（外形图）/ HD-1910-C001（产品页） |
| 电压 | **5–8.4 V** |
| 尺寸 | 34 × 20 × 23 mm（深度比 XL330 的 26 mm 少约 3 mm） |
| 重量 | 22.5 ± 2 g |
| 堵转扭矩 | **10 kg·cm**（≈ 0.98 N·m） |
| 额定负载 | **3.0 kg·cm**（≈ 0.29 N·m） |
| 空载转速 | 110 rpm |
| 电流 | 待机 21 / 空载 140 / 额定 500 / 堵转 1800 mA |
| 接口 | AMP-3：1=GND · 2=Vcc · 3=Signal/TTL |
| 编码器 | 12-bit 磁编码（同 HL 平台叙述） |
| 波特率 | 与 HL 同平台则至 1 Mbps（产品页未单独印死） |
| 协议 | 飞特 TTL 半双工（非 DXL 2.0） |

证据：飞特产品页电气 + OpenMicroDuck `hardware_spec/servo/HD-1910M-C001-drawing-20260902.pdf`（**外形图，非电气规格书**）。本地仓：`OpenMicroDuck/`。

## 与其它候选

- 伺泰威 ED330：多组电流数字与 HD-1910 相同，但额定负载写成 **0.8 kg·cm** —— **勿当第二货源**，待实测。
- [[feetech-hl-2909]] / HL-2915：12 V 档，供电与 HAT 改动更大。
- 换执行器必须 **重训** 策略；官方 ONNX 不能 bit-exact 复用。

相关：[[feetech]] · [[feetech-hl-2909]] · [[xl330-vs-feetech-servos]] · [[openmicroduck]]
