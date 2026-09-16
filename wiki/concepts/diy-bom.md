---
title: DIY BOM（v0.1 汇总）
created: 2026-09-03
updated: 2026-09-11
type: concept
tags: [diy, bom, mechanical, board]
sources:
  - concepts/mechanical-bom-rl.md
  - concepts/print-bom-rl.md
  - concepts/seeed-bearings.md
  - concepts/fastener-bom-study.md
  - entities/microduck-diy.md
confidence: high
related:
  - microduck-diy
  - diy-milestones
  - print-bom-rl
  - mechanical-bom-rl
  - seeed-bearings
  - fastener-bom-study
  - dynamixel-xl330
  - radxa-zero-3w
  - elec-rpi-robot-hat
  - imu-to-dxl-v2
  - imu-to-dxl-ref-bom
  - elec-hat-lcsc-order-2026-09-05
  - imu-to-dxl-lcsc-order-2026-09-09
  - imu-to-dxl-lcsc-order-2026-09-05
  - robotis-xl330-order-2026-09-05
  - taobao-diy-procurement-2026-09
  - board-interconnect
  - elec-three-boards
  - board-hat
  - board-imu-to-dxl
---

# DIY BOM（v0.1）

面向 [[microduck-diy]] 的**采购/打印/装配总表**。网格与数量来自 [[mechanical-bom-rl]] / [[print-bom-rl]]；**不是**官方量产装箱单。里程碑见 [[diy-milestones]]。

| 阶段 | 本页覆盖 |
|------|----------|
| **现行** | 打印件 + 轴承 + 紧固件示意 + 15× 舵机 + HAT + 机身 IMU v0.3 |
| 后置 | 相机、ToF、音频、NFC 等扩展 |

> 装机定稿：[[board-interconnect]] · [[elec-three-boards]]；机身 IMU 测试 **1 号/2 号** → [[board-imu-to-dxl]]。

## A. 3D 打印 · 硬质（PETG/ASA）

数量按 RL 入结构实例；明细命名见 [[print-bom-rl]]。

| 件名 | 数量 | 备注 |
|------|------|------|
| `left_shell` / `right_shell` | 1+1 | 勿用旧名 `trunk_shell_*` |
| `top_head_shell` / `bottom_head_shell` | 1+1 | |
| `face_part` | 1 | |
| `trunk_base` | 1 | |
| `motor_support` / `power_support` | 1+1 | |
| `banana_pcb_locker` | 1 | |
| `upper_leg_left` / `upper_leg_right` | 1+1 | 勿用旧 `left/right_upper_leg` |
| `upper_leg_rigidity_plate` | 2 | |
| `leg` / `hip_l` | 2+2 | |
| `ankle_left` / `ankle_right` | 1+1 | |
| `foot_left` / `foot_right` | 1+1 | |
| `neck` | 2 | |
| `neck_pitch` | 1 | |
| `yaw2roll` | 2 | |
| `yaw_roll_motion` | 1 | |
| `jaw` | 1 | |
| `m12_lens_holder` / `noenoeil` | 1+1 | 相机后置也可先打 |

**硬质小计：30 件。** 资料：`microduck-diy/cad/*.3mf`。

## B. 3D 打印 · 软胶（TPU 90–95A）

| 件名 | 数量 |
|------|------|
| `sole_left` / `sole_right` | 1+1 |
| `jaw_soft` / `soft_mouth_top` | 1+1 |

**软胶小计：4 件。**

## C. 外购 · 执行器与轴承（M1）

| 物料 | 规格/型号 | 数量 | 说明 |
|------|-----------|------|------|
| 舵机 | [[dynamixel-xl330]]（XL330-M288-T） | **15** | **主单** [[robotis-xl330-order-2026-09-05]]；另淘宝样机+套件 → [[taobao-diy-procurement-2026-09]] |
| 法兰螺丝（horn） | **PHS M2×6 TAP** | **6**/台 → 整机 **90** | 随舵机装箱「Bolts for horns」 |
| 机身框架螺丝 | **PHS M2×8 TAP** | **10**/台 → 整机 **150** | 随舵机装箱「Bolts for frames」；**不是**法兰钉 |
| 薄壁轴承 | 16×22×4（[[seeed-bearings]]） | **11** | 淘宝已购 **11**（10+1）· [链接](https://item.taobao.com/item.htm?id=930534977802) |
| 小轴承 | ~10×15×3（约 6700 档） | **3** | 淘宝已购 **3** · 同上 |
| 滚道位 | `bearing_roll` | 2 | 按实机另配；可先打实心占位 |

> **PHS** = Pan Head Screw（圆头十字）；**TAP** = 塑壳自攻/螺纹成型钉。正品舵机通常已随包装附带；散装补购时按上表型号买，勿用普通机牙 M2 硬拧塑壳。金属 horn 套装（HNX330-N101）另配 PHS M2×4，与法兰钉不同。

实心打印占位仅作装配预演，非真轴承。

## D. 紧固件 · 结构件（M1 · 示意）

摘自 [[fastener-bom-study]]，**非官方真实数**（不含上表舵机原厂钉）。初样建议：

| 规格 | 用途 | 数量级 |
|------|------|--------|
| M2×4 / ×6 / ×8 | 壳、门、脚、支架 | 淘宝 09-01～04 已购多包 · [[taobao-diy-procurement-2026-09]] |
| M2 热熔铜螺母 | 打印凸台 | 已购若干 · 同上 |
| Ø2 销 | 定位 | ~6 |

整机粗估约 **110–160** 颗结构钉 + 舵机原厂钉（90+150）。采购前按孔位复核。

## E. 电控最小集（M2 · →v0.3）

| 物料 | 选型 | 数量 | 状态 |
|------|------|------|------|
| 主控（**头舱**） | [[radxa-zero-3w]] | 1 | 淘宝 08-29 · [ZERO 3W](https://item.taobao.com/item.htm?id=746425059858) · ⏳ |
| 电源+DXL HAT（**头舱**） | [[elec-rpi-robot-hat]] / [[elec-hat-lcsc-order-2026-09-05]] | 1 | 含板载 **BMI088=头 IMU** · 立创+淘宝 · [[taobao-diy-procurement-2026-09]] · 配料焊 [[hat-solder-kit]] · ⏳ |
| 机身 IMU（**测试 1 号 · v0.3**） | [[board-imu-to-dxl]] / [[imu-to-dxl-ref-bom]] | 打样 | 立创 **`SO26090921960`** + 配单 **`BOM260909006316`** · ⏳；**缺 BM07（C160393）** → [[imu-to-dxl-lcsc-order-2026-09-09]] |
| 电池 | [[np-f550-battery]]（沣标 2200 mAh×2 + 双充） | 1 套 | 淘宝 **09-11 已付款** · [[taobao-diy-procurement-2026-09]]；组装拆充电极装 **`power_support`** · 台架仍可用 XT30↔Type-C · [[bench-power-supply]] |

网格占位件（`elec_rpi_robot_hat_pcb` 等）：**勿当真机打印件**。

## F. 后置（非 v0.1 必达）

| 物料 | 选型 | 说明 |
|------|------|------|
| 相机 / ToF / 音频 / NFC | [[imx219-camera]] · [[vl53-tof]] 等 | Camera V2 已购 · [[taobao-diy-procurement-2026-09]] |

## 对照速查

| 问 | 去哪 |
|----|------|
| 网格种类/实例数 | [[mechanical-bom-rl]] |
| 打印料色/切片 | [[print-bom-rl]] |
| 轴承 | [[seeed-bearings]] |
| 螺丝 | [[fastener-bom-study]] |
| XL330 | [[robotis-xl330-order-2026-09-05]] |
| 淘宝 | [[taobao-diy-procurement-2026-09]] |
| 接线 | [[board-interconnect]] |
| 机身 IMU v0.3 | [[imu-to-dxl-ref-bom]] · [[imu-to-dxl-lcsc-order-2026-09-09]] |
| 头 IMU | [[board-hat]]（BMI088） |
| 电控板 | [[elec-three-boards]] |
| 合并 CSV | [[elec-three-board-bom]] |
| 里程碑 | [[diy-milestones]] |

相关：[[microduck-diy]] · [[diy-milestones]] · [[robotis-xl330-order-2026-09-05]] · [[print-bom-rl]]
