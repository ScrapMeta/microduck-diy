---
title: Dynamixel XL330
created: 2026-08-30
updated: 2026-09-16
type: entity
tags: [servo, dynamixel]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/transcripts/research-hardware-servos-2026-08.md
  - raw/articles/robotis-xl330-order-b260905014mp-2026-09-05.md
  - raw/articles/xl330-cn-starter-kit-notes-2026-09-10.md
  - https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/
confidence: high
related: [elec-rpi-robot-hat, imu-to-dxl-v2, diy-bom, robotis-xl330-order-2026-09-05, xl330-cn-bench-kit, robotis, body-imu-hat-dxl-power-eval, hat-dxl-bus-debug]
---

# Dynamixel XL330（M288-T）

Microduck **15 关节**执行器。典型 **XL330-M288-T**：20×34×26 mm，18 g，3.7–6 V，堵转约 0.52 N·m（~5.3 kg·cm）@5 V，塑料齿，Protocol **2.0** TTL。软件：`rustypot` / `Xl330Controller`。

规格书：[eManual XL330-M288](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)

## 项目内用法

- 总线经 [[elec-rpi-robot-hat]]；与 [[imu-to-dxl-v2]] 共线
- 产线写 ID/参数；现场一般不刷
- 仿真摩擦：[[better-actuator-models-bam]] 有 **XL330-288-T** 模型
- 实机母线：官方常跟 [[np-f550-battery]]（约 6.6–8.2 V），**高于手册 6.0 V 上限**。  
  **DIY 实测（2026-09-15）：** ~**7.2 V** 红灯持续闪（过压报警）；~**6.5 V** 上电闪一下后正常。装机/台架母线建议 **6.0–6.5 V**（**6.0 V 优先**）粗线进 HAT，见 [[body-imu-hat-dxl-power-eval]]。

## 手册要点（XL330-M288 · 权威）

来源：[eManual](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)（2026-09-16 取）。控制表地址即 `scripts/dxl_ping.py` 所读。

| 项 | 值 |
|----|-----|
| `Input Voltage` | **3.7–6.0 V（推荐 5.0 V）** |
| `Max Voltage Limit(32)` | 默认 **70 = 7.0 V**（可设 31–70）；超出即置 Input Voltage Error |
| `Min Voltage Limit(34)` | 默认 35 = 3.5 V |
| Protocol | **2.0**（`Protocol Type(13)` 默认 2） |
| `Baud Rate(8)` | 值 **1(Default) = 57 600**；**3 = 1 Mbps**（本总线） |
| 出厂默认 | **ID 1** · **57 600** · `Return Delay Time=250` · `Shutdown=53` · `PWM Slope=140` |
| `robotd` 写值 | `return_delay_time=0` · `baud_rate=3` · `pwm_slope=255` · **`shutdown=52`** |

### `Shutdown(63)` 位（决定「哪些故障会锁 torque off」）

| bit | 值 | 含义 |
|-----|----|------|
| 0 | 0x01 | **Input Voltage Error**（出厂默认 53 **含**此位） |
| 2 | 0x04 | Overheating |
| 4 | 0x10 | Electrical Shock |
| 5 | 0x20 | Overload |

- 出厂 **53** = bit0+bit2+bit4+bit5；`robotd` 写 **52** = **去掉 bit0** → **官方配置并不锁 input-voltage**
  （旧说法「`shutdown=52` 锁存过压」是**反的**；该说法见于 `robotd-design` §2.1 散文，与手册位表冲突，以手册为准）。
- 触发 `Shutdown` → `Torque Enable(64)` 清 0、**红灯持续闪**（手册：*Shutdown Error → LED blinks continuously*），须**重启/REBOOT 指令**才恢复。
- **过压是「转动」失效、不是「通信」失效**：处于 shutdown 的舵机**仍应答 Ping/Read**。别把「不动」读成「零回包」。

## DIY 采购 / 台架

| 路径 | 说明 |
|------|------|
| Robotis 直邮 | 订单 **B260905014MP**：15× · [[robotis-xl330-order-2026-09-05]] |
| **CN 台架** | **XL330-M288-T-CN** + 国产 U2D2/PHB · [[xl330-cn-bench-kit]]（**✅ 通过** · 明细后补） |

相关：[[diy-bom]] · [[xl330-cn-bench-kit]] · [[robotis-xl330-order-2026-09-05]] · [[robotis]] · [[body-imu-hat-dxl-power-eval]]
