---
title: VL53 ToF（头部 8×8 测距）
created: 2026-08-30
updated: 2026-09-19
type: entity
tags: [tof]
sources: [raw/articles/workspace-readme-hardware-2026-08-29.md]
confidence: medium
---

# VL53L5CX / VL53L8CX（8×8 多区 ToF）

> **⚠️ 别再叫它「激光雷达」**。原厂 Press Kit 写的是 *compact LiDAR*，但**它不是 LiDAR** ——
> 是 ST 的 **8×8 多区 ToF**（DToF，非扫描式）。选型/询价请按 ToF 的关键词找，
> 按「LiDAR」去找会拿到完全不同的东西（机械旋转/固态扫描，价格与接口都不是一档）。

头部测距，经 [[elec-rpi-robot-hat]] 的 **J5 Stemma/Qwiic** 接出。软件在 `refs/microduck/tof`。

## 型号与规格（2026-09-19 核对）

| 项 | 值 | 依据 |
|----|-----|------|
| 型号 | **VL53L8CX** 或 **VL53L5CX**，固件两者都支持 | `tof/src/sensor.rs:70-89` 按 revision byte 自动识别：`0x0C = L8cx` / `0x02 = L5cx` |
| **在役机器装的是哪颗** | **多数是 L5CX**（旧款） | `sensor.rs:76` 注释原文：revision `0x02` 是 *"the older sensor, and **the one most ducks in the field have**"* |
| 分区 | **8 × 8 = 64 区** | 同上 |
| 视场 | **45° × 45°**（对角 63°） | `refs/microduck_rl/src/mjlab_microduck/sim/tof.py:3,28` |
| 量程 | **4 m** | 同上 |
| 数据率 | **15 Hz** 矩阵流 | `sim/tof.py:3`；拆解文档（切硬件 I²C 后才做到，此前 bit-bang 烧 CPU） |
| 接口 | **JST SH 1.0 mm 4P**（Stemma/Qwiic），挂 **J5** | HAT J5–J8 均可 |
| I²C | **`0x29`**（两代出厂默认）或 **`0x52`** | `tof/src/main.rs:102-107`：`0x52` 是原型期为避让一颗要 `0x29` 的 I²C IMU 而改的，**该 IMU 已移除，但改过地址的传感器地址掉电不丢** |
| 总线速率 | **400 kHz**（上限） | 被 codec 与 BMI088 拖住；VL53 本身能跑 1 MHz |
| 上电 | 需经 I²C 灌约 **90 KB** 固件到传感器 RAM | [[firmware-flash-matrix]]（每次启动） |
| 量产用哪颗 | **官方未钉** | 官方只公布「8×8」；复刻仓已购 **VL53L8CX**（`refs/microduck-replica/调试记录.md:41`） |

> **⚠️ 采购含义（容易被忽略）**：固件是**两代兼容**的，但**在役机器多数装 L5CX**
> （`sensor.rs:76` 原文 *"the one most ducks in the field have"*）。
> 所以「照着一台真机买同款」你大概率会买到 **L5CX**；L8CX 是更新的一代、引脚与接口兼容。
> **两者都不要用「激光雷达」去搜。**

## 尺寸

| 层级 | 尺寸 | 来源 |
|------|------|------|
| **裸芯片**（LGA 封装） | **6.4 × 3.0 × 1.75 mm** | ST 数据手册 —— ⚠️ **仓库内无此数据**，来自芯片手册 |
| **breakout 模块** | **未钉**，取决于买谁家的板子 | ⚠️ **这是唯一缺的尺寸** |

**关键**：原厂用的是 **breakout 模块**（否则接不出 Stemma 4P），但**原厂 BOM 没钉模块型号**，
所以模块外形尺寸**没有权威值** —— 按手头空间自选（Adafruit / 微视 / DFRobot 等都有带 Stemma 的板子）。

## 采购坑（引自复刻仓踩坑记录）

- **别买成 VL53L0X** —— 搜「VL53L5CX」出来的绝大多数是 **VL53L0X（单点测距）**，**固件不认**。
- **VL53L7CX ≠ VL53L8CX** —— L7 是 90° 视场的另一颗；部分链接把 L7/L8 混在一个宝贝里，**选 SKU 看清**。
- 有条 ¥8 的「VL53L5CX」标题里还写着「79 GHz 雷达传感器」—— 关键词堆砌的坑货。

相关：[[board-interconnect]] · [[firmware-flash-matrix]] · [[microduck]]
