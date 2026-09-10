---
title: 板级接线与装机拓扑
created: 2026-08-30
updated: 2026-09-09
type: concept
tags: [board, hat, power]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - concepts/board-hat.md
  - concepts/board-imu-to-dxl.md
confidence: high
related:
  - elec-three-boards
  - board-hat
  - board-imu-to-dxl
  - radxa-zero-3w
  - dynamixel-xl330
  - diy-bom
---

# 板级接线与装机拓扑

> **现行 DIY 定稿（2026-09-09）。** 板卡入口：[[elec-three-boards]]。

## 1. 装机位置（已定）

| 位置 | 板 / 器件 | 说明 |
|------|-----------|------|
| **头部** | [[radxa-zero-3w]] + [[board-hat]] 叠装 | 主控与 HAT **同在头舱** |
| **头部** | HAT 板载 **BMI088** | DIY 头 IMU；不另做专板 |
| **机身** | 机身 IMU ID **200** | 测试 **1 号或 2 号**（不同时上机）；两髋上方 |
| **全身** | 15× [[dynamixel-xl330]] | 与机身 IMU **同一条** TTL |

### 机身 IMU 测试板（统一设定）

| 板 | 外形 | DXL | 固定 | 接线角色 |
|----|------|-----|------|----------|
| **1 号大板** | **32×22** | **2× 3P** | 四角 φ2.2 · 孔距 29×19 | 可中继；下游宜少 |
| **2 号小板** | **22×15** | **1× 3P** | **两边中心 M2** | **线 B 链尾 / 叶子** |

规格全文：[[board-imu-to-dxl]]。

J13/J14 = **同一条总线的两个插座**。针脚：**1=GND · 2=VBATT · 3=DATA**。

## 2. 系统总图（电源 / 非 DXL）

```
NP-F550（机身）──电源线──► HAT（头舱）
                            ├─ 40-pin ──► Zero 3W
                            ├─ J13 / J14 ──► 见 §3 DXL
                            ├─ BMI088（头 IMU）
                            ├─ Qwiic ──► ToF（可选）
                            └─ 音频
摄像头 ──CSI──► Zero（不经 HAT）
```

## 3. DXL 怎么接（推荐拓扑）

HAT 在**头**里，线必须先经过颈头区域再下到腿——所以**不能**两腿各 5、颈头再「随便挂空的一口」还保持两边一样多。颈头 5 颗只能串进其中一根线，**故意不对称**：

| 线 | HAT 口 | 设备顺序（菊花链） | 数量 |
|----|--------|-------------------|------|
| **线 A** | J13 | **30→31→32→33→34 → 20→21→22→23→24** | 10 |
| **线 B** | J14 | **10→11→12→13→14 → 200（机身 IMU）** | 6 |

- 软件只认 ID，**不在乎**哪边颗数多。
- 线 A 先串颈头（离 HAT 近），再下左腿。
- 线 B 只走右腿，**链尾**接机身 IMU（见 §4）。

### 示意图

```
                         ┌─ Radxa Zero 3W
                         │
                    ┌────┴─────┐
                    │   HAT    │  ← 头舱
                    │  J13 J14 │
                    └────┬─────┘
               线A        │        线B
            (J13)         │         (J14)
               │          │          │
               ▼          │          ▼
            30 neck_pitch │       10 right_hip_yaw
               │          │          │
            31 head_pitch │       11 right_hip_roll
               │          │          │
            32 head_yaw   │       12 right_hip_pitch
               │          │          │
            33 head_roll  │       13 right_knee
               │          │          │
            34 mouth      │       14 right_ankle
               │          │          │
            20 left_hip_yaw│         │
               │          │          ▼
            21 left_hip_roll│    200 机身 IMU ← 单 3P 链尾
               │          │       （髋部上方；短线从踝旁折回髋，
            22 left_hip_pitch│      或见下方「更好的链尾位置」）
               │          │
            23 left_knee  │
               │          │
            24 left_ankle │
```

### 机身 IMU 接法（单 3P）— 不必专门买「三通」

**最简单（推荐先这样做）：** 线 B 按 `10→11→12→13→14→200` 串到底，IMU 用**一根普通 3P 线**插在右踝舵机空闲口上当链尾。板仍用螺丝固定在两髋中间——线从腿侧走到髋部即可（多几厘米线，无额外零件）。

单 3P 的 IMU **不能**插在链**中间**（没有第二口续给下游）。要么链尾，要么下面说的分叉，要么板上两个 EH 做中继。

**可选：「3P 三通 / Y」是什么？**

不是 HAT 上的端口，也不是舵机自带端子。指一根**自制或外购的分叉线束**：三根线（GND / VBATT / DATA）在中间**并联**成「一进两出」，让总线在髋旁同时接到右腿链和 IMU：

```
        ┌─ 3P 插头 ──► 右腿 10→…→14
HAT/上游┤
        └─ 3P 插头 ──► IMU 200（叶子）
```

常见来源：① 两根 Robotis **Robot Cable-X3P**（或 JST EH 3P 线）剥开后把同名脚焊/压在一起；② 淘宝「Dynamixel 3P Y 线 / 一分二」类线材（注意要 **TTL 3P**，不是 RS-485 4P）。**没有也不影响装机**——用上面的链尾接法即可。

## 4. 机身 IMU：单 3P vs 双 3P

| 板 | 接法 |
|----|------|
| **2 号**（单 3P） | 必须为线 B **链尾/叶子**；普通 3P 线即可，不必买三通 |
| **1 号**（双 3P） | 可中继；测试时下游舵机宜少，避免大电流穿板 |

勿让 15 舵机电流穿堂过 IMU 铜箔。固件：测试板默认 **1G125**。

## 5. 头 IMU

HAT **BMI088**，无额外 DXL 线。控制环仍只认 ID **200**。

## 6. 相关页

[[board-hat]] · [[board-imu-to-dxl]] · [[diy-bom]] · [[elec-three-boards]] · [[dual-imu-board-selection]]

相关：[[firmware-flash-matrix]] · [[opensource-coverage]] · [[dynamixel-xl330]]
