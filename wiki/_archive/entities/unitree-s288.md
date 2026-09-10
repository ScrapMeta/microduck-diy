---
title: Unitree S288（YS-342026-S288）
created: 2026-08-31
updated: 2026-08-31
type: entity
tags: [servo, unitree]
sources:
  - https://shop.unitree.com/products/brushless-digital-servo
  - https://aifitlab-wiki.super.site/unitree-motor-docs/unitree-brushless-digital-servo-motor-user-manual
  - https://github.com/unitreerobotics/digital_servo
confidence: high
---

# Unitree S288（YS-342026-S288）

宇树 **无刷数字舵机**（塑壳 / 塑料齿版）；金属齿铝壳为 **J288**（同协议、更高压档）。

## 规格摘要

| 项 | S288 |
|----|------|
| 外形 | 20×34×26 mm（与 XL330 同档） |
| 重量 | 19.5 g |
| 减速比 | **288.35 : 1** |
| 电压 | 最低 **6.4 V**；推荐 **12.6 V**；最高 12.6 V |
| 协议 | **宇树自定义**半双工 TTL 总线（非 Dynamixel） |
| 波特率 | **6 Mbps**（固定，不可配） |
| 帧格式 | 8N1 |
| 总线 ID | **0–14**（最多 16 台；15 为广播） |
| 控制包 / 反馈 | 20 B（`0xFE 0xEE`）/ 26 B（`0xFC 0xEE`），CRC32 |
| 控制模式 | 混合闭环：转子侧力矩、位置、速度 + 刚度 Kp、阻尼 Kd |
| 连接器 | TTL 多点总线（3 芯概念与 DXL TTL 类似，**协议不同**） |

公开资料：[Unitree 商店](https://shop.unitree.com/products/brushless-digital-servo)、[digital_servo 仓库 protocol.md](https://github.com/unitreerobotics/digital_servo/blob/main/specs/protocol.md)。

## 与 Microduck 关系

**不能作为 XL330 平替** — 见 [[xl330-vs-unitree-s288]]。

相关：[[dynamixel-xl330]] · [[unitree]] · [[xl330-vs-feetech-servos]]
