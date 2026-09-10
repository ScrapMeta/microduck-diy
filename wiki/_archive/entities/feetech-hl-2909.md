---
title: Feetech HL-2909
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
  - feetech-hl-2915
  - feetech-hd-1910
  - dynamixel-xl330
  - xl330-vs-feetech-servos
  - openmicroduck
---

# Feetech HL-2909（HL-2909-C001）

飞特 **12 V 级** TTL 串行舵机。[[openmicroduck]] 样机用 **HL-2909** 验证结构与协议。

## 命名关系

- 用户侧说明：**HL-2915-C002 为曾用名**（同平台规格书封面写 HL-2915-C002）。
- 规格书文件：`HL-2915-C002_HL-2909-C001串型规格书-20260227.pdf`（OpenMicroDuck `hardware_spec/servo/`）。
- 正文**无**单独「2909」参数表；下表按该 **A/0 · 2026-02-27** 规格书（OpenMicroDuck 摘录）。
- 本 wiki 另有早期页 [[feetech-hl-2915]]（口述/旧笔记，扭矩口径不同）—— **以规格书 PDF 为准**，冲突时标 contested。

## 参数（规格书摘录）

| 项 | 值 |
|----|-----|
| 电压 | **9–14 V**（额定 12 V） |
| 尺寸 | 34 × 20 × 23 mm |
| 重量 | 22.5 ± 2 g |
| 减速比 | 320 : 1 |
| 堵转扭矩 | **8.9 kg·cm @ 12 V**（≈ 0.87 N·m） |
| 额定扭矩 | **2.9 kg·cm**（≈ 0.28 N·m，约 1/3 堵转） |
| 空载转速 | 77 rpm @ 12 V |
| 电流 | 待机 42 / 空载 140 / 额定 200 / 堵转 600 mA @ 12 V |
| 接口 | AMP-3（与 HD-1910 同针序） |
| 协议 | 半双工 8N1，飞特包；出厂默认 **1 Mbps** |
| 编码器 | 12-bit 磁编码 |
| ID | 0–253（出厂常为 1） |
| 恒力 | 模式 2 恒流；地址 44 恒力输出（规格书） |

## 对 Microduck / DIY 的含义

- 电压属 **12 V 轨**：电池串数或升压、HAT MOSFET、总线铜箔与 `imu_to_dxl` 取电都要按 12 V 重算；比 [[feetech-hd-1910]]（5–8.4 V）改动大。
- 协议非 DXL → 官方 `robotd` 不能直接驱动；OpenMicroDuck 走飞特兼容栈。
- 外形与 XL330 同档但深度 23 mm vs 26 mm，孔距需实物核。

相关：[[feetech-hd-1910]] · [[feetech-hl-2915]] · [[xl330-vs-feetech-servos]] · [[openmicroduck]] · [[feetech]]
