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
  官方 2S 直供**能跑**的机制是 `robotd` 写 `shutdown=52`（**清掉** bit0 Input Voltage Error）——即**关掉过压保护**，不是解决了电压；见下「母线电压天花板」。

## 手册要点（XL330-M288 · 权威）

来源：[eManual](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)（2026-09-16 取）。控制表地址即 `scripts/dxl_ping.py` 所读。

| 项 | 值 |
|----|-----|
| `Input Voltage` | **3.7–6.0 V（推荐 5.0 V）** |
| `Max Voltage Limit(32)` | 默认 **70 = 7.0 V**；可设范围 **31–70（3.1–7.0 V）**，**只能调低**；超出即置 Input Voltage Error |
| `Min Voltage Limit(34)` | 默认 35 = 3.5 V |
| `Operating Mode(11)` | 默认 **3 = Position Control**；`robotd` **不写**此寄存器 → 决定哪个限幅生效（见下） |
| `Current Limit(38)` | 默认 **1750 = 1.75 A**，可设上限同样 1750（≈ 6.0 V 堵转 1.74 A）；**只在 Current Control(0) / Current-based Position(5) 生效** |
| `PWM Limit(36)` | 默认 **885 = 100 %**；**所有模式**的输出限幅 |
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

### 母线电压：7.0 V 是固件天花板（8.4 V 无寄存器解）

`Max Voltage Limit(32)` **能改，但只能往下改**：范围 **31–70 → 3.1–7.0 V**。
写 70 只是把报警门槛抬到最高，**8.4 V 依然必然置位** Input Voltage Error ——
该寄存器是**比较器的跳闸点，不是稳压器**：H 桥 / 母线电容 / 电机绕组看到的仍是 8.4 V。
**没有任何寄存器值能把 8.4 V 变成合规。**

8.4 V 下的实际行为分两支，取决于 `Shutdown(63)` bit0：

| `Shutdown(63)` bit0 | 行为 | 后果 |
|---------------------|------|------|
| **置位**（出厂 **53**） | `Torque Enable(64)`→0，输出 0 %，**锁存、须 REBOOT** | 满电 8.4 V **整机瘫**；要等电池落到 7.0 V 以下，且**不自恢复** |
| **清零**（`robotd` 写 **52**） | 不切扭矩，照跑 | **静默超压**：被拿掉的正是过压保护这一位，错误位与 Alert(0x80) 长置 |

> **推论（重要）**：官方整机在 2S 上跑，靠的是**清掉 bit0**，不是解决了电压。
> 谁把 `shutdown` 改回出厂 **53**，谁就把机器人变成「满电不能用」。
> 台架那颗 CN 舵机**现在就是 53**（2026-09-16 实测）→ 母线一旦超 7.0 V 即 torque off。

**哪个限幅生效取决于 `Operating Mode(11)`**（默认 **3**，`robotd` 不写它）：

| 模式 | 输出限幅 | 升压到 8.4 V 的后果 |
|------|----------|---------------------|
| **3 Position Control**（出厂默认） | `PWM Limit(36)` | `Current Limit(38)` **不生效** → 输入电流可超 1.74 A / 6.0 V 额定，**1.75 A 天花板不保护你** |
| 0 / 5 Current(-based Position) | `Current Limit(38)` | 扭矩被 1.75 A 钉住 |

→ **先读 `Operating Mode(11)`，再谈「8.4 V 能不能用」**。
`scripts/dxl_ping.py info` 自 2026-09-18 起读该寄存器（[[dxl-bench-method]] · `scripts/README.md`）。

## DIY 采购 / 台架
| 路径 | 说明 |
|------|------|
| Robotis 直邮 | 订单 **B260905014MP**：15× · [[robotis-xl330-order-2026-09-05]] |
| **CN 台架** | **XL330-M288-T-CN** + 国产 U2D2/PHB · [[xl330-cn-bench-kit]]（**✅ 通过** · 明细后补） |

相关：[[diy-bom]] · [[xl330-cn-bench-kit]] · [[robotis-xl330-order-2026-09-05]] · [[robotis]] · [[body-imu-hat-dxl-power-eval]]
