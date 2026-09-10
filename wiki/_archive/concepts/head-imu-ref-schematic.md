---
title: 头部 IMU 参考板设计
created: 2026-09-04
updated: 2026-09-06
type: concept
tags: [imu, board, jlceda]
confidence: medium
related: [board-imu-head, elec-three-boards, dual-imu-board-selection, imu-to-dxl-v2, elec-rpi-robot-hat, board-interconnect, vl53-tof, head-imu-ref-bom, imu-to-dxl-ref-bom, imu-to-dxl-ref-pcb-layout]
---

# 头部 IMU 参考板设计

> **REFERENCE — NOT OFFICIAL**  
> **现行定稿丝印：`imu-head v0.2` · huodianyan · `260905`。**  
> **板信息卡（总览）：** [[board-imu-head]] · [[elec-three-boards]]  
> 官方未公开头 IMU 原理图/芯片。本页按 Press Kit「双 IMU」+ MJCF `head_imu` + HAT **STEMMA QT / Qwiic** 生态做的复刻规格。  
> **控制环不用本板**（只认机身 [[imu-to-dxl-v2]] ID 200）；本板供头姿/交互/实验。

工程建议名：`head_imu_ref` / 丝印 `imu-head` · 单页原理图。选型背景见 [[dual-imu-board-selection]] §3。

## v0.2 定稿变更（相对 v0.1）

| 项 | 说明 |
|----|------|
| 芯片 | 与机身统一 **LSM6DSV16X**（lwimu） |
| 插头 | **BM04B-SRSS-TB 4P**（与机身 SWD / HAT STEMMA 同座系） |
| 丝印 | **IMU X/Y 坐标轴**；版号 v0.2 |

## 截图（v0.2 · 2026-09-05）

| 图 | 文件 |
|----|------|
| PCB 布线 | [`imu-head-v0.2-pcb-2026-09-05.png`](../assets/pcb/imu-head-v0.2-pcb-2026-09-05.png) |
| 3D 正面 | [`imu-head-v0.2-3d-2026-09-05.png`](../assets/pcb/imu-head-v0.2-3d-2026-09-05.png) |
| 历史 v0.1 | `imu-head-v0.1-{sch,pcb,3d}-2026-09-05.png` |

![3D v0.2](../assets/pcb/imu-head-v0.2-3d-2026-09-05.png)

![PCB v0.2](../assets/pcb/imu-head-v0.2-pcb-2026-09-05.png)

## 1. 定位与约束

| 项 | 规格 |
|----|------|
| 角色 | 头内 6 轴，**I²C 从机模块**（无 MCU、无 DXL） |
| 结构 site | `head_imu`（RL：`jaw_soft` 附近） |
| 板框目标 | **18×14 mm**（厚 **0.8–1.0 mm**；占位曾用 18×14×3） |
| 供电 | 仅 **+3V3**（来自 HAT Qwiic，勿挂 VBATT） |
| 总线 | 与 ToF **同 I²C 域**；地址勿撞 VL53（常 0x29） |
| 接口 | 对齐 HAT：**JST-SH 1.0 mm · BM04B-SRSS-TB**（STEMMA QT） |

**不做：** DXL 从机、高压 LDO、SWD、音频、BMI088 替机身控制。

## 2. 功能块

```
HAT Qwiic / STEMMA QT
  GND · +3V3 · SDA · SCL （可选 INT 经第 5 线或测试点）
        │
        ▼
   J1 BM04B-SRSS-TB
        │
        ├─ R1/R2 上拉（默认 DNP，HAT 侧通常已有）
        ├─ C1/C2 去耦
        └─ U1 LSM6DSV16XTR（I²C）
              SA0→GND → 地址 0x6A
              INT1 → TP1（或 J1-5 若改 5P）
```

## 3. BOM（摘要）

完整料号 / DNP / 采购合并 → [[head-imu-ref-bom]]。

| Ref | 型号 | 贴装 | 作用 |
|-----|------|------|------|
| U1 | LSM6DSV16XTR | 必贴 | 6 轴 I²C · 0x6A |
| J1 | BM04B-SRSS-TB | 必贴 | STEMMA QT 4P |
| C1–C3 | 100n×2 + 1µ | 必贴 | 去耦 / bulk |
| R1/R2 | 10 k（C25744） | **DNP** | I²C 上拉（HAT 已有则不焊） |

## 4. 连接器线序（J1）

与常见 STEMMA QT / Qwiic 一致（核对 HAT 丝印）：

| Pin | 网络 | 说明 |
|-----|------|------|
| 1 | GND | |
| 2 | +3V3 | |
| 3 | SDA | → U1 SDA |
| 4 | SCL | → U1 SCL |

若改 **BM05B** 5P：pin5 = `IMU_INT` ← U1 INT1。

## 5. U1 接线（I²C）

| U1 脚 | 网络 |
|-------|------|
| Vdd / Vdd_IO | +3V3（各旁路 100 nF） |
| GND | GND |
| SDA / SCL | SDA / SCL |
| CS | **+3V3**（拉高选 I²C，勿悬空） |
| SDO/SA0 | **GND** → 7-bit **0x6A**（接 3V3 则为 0x6B） |
| SCx/SDx（辅） | NC 或按手册接固定电平 |
| INT1 | TP1（可选出线） |
| INT2 | NC |

SPI 相关脚按数据手册在 I²C 模式下接好，避免浮空。

## 6. PCB 摆放（18×14）

示意图：[`assets/pcb/head-imu-placement.svg`](../assets/pcb/head-imu-placement.svg)

```
        ← 18 mm →
┌─────────────────────┐
│ J1 SH-4P（短边出线） │
│  C3                 │  ≈14 mm
│     U1 LSM6DSV      │
│   C1 C2   R1/R2 DNP │
│              TP1    │
└─────────────────────┘
```

| 优先级 | 做法 |
|--------|------|
| 1 | U1 居中，远离板边挠曲 |
| 2 | C1/C2 贴 U1 电源脚；C3 近 J1 的 3V3 |
| 3 | J1 短边外侧，针朝外，线束向 HAT/头腔 |
| 4 | 底层完整 GND；I²C 短；R1/R2 标 DNP |
| 5 | TP1 用**小焊盘**（勿用 Ø3.2 大通孔占板） |
| 6 | 丝印：`head_imu_ref` · `0x6A` · 轴箭头 +X/+Y/+Z |

朝向：头内安装见下节；**不做**机身板那套 DXL `DEFAULT_MOUNT`。软件侧自行标定或固定旋转矩阵。

### 6.1 结构位置（MJCF site `head_imu`）

官方无板外形，仅有传感器 site（单位 m → mm）：

| 来源 | 父连杆 | 约 (x, y, z) mm | site quat |
|------|--------|-----------------|-----------|
| RL `robot_walk.xml` | `jaw_soft` | **(+15.2, +0.1, −51.1)** | 单位四元数（与父系对齐） |
| alpha `robot_walk.xml` | `bottom_head_shell` | **(+11.5, +0.2, −51.3)** | 单位四元数 |

同框参考：`head_camera` / `tof` 约 z≈**−73**，比 IMU 更靠脸侧；IMU 在**矢状面中线附近（y≈0）**、略偏父系 +x、深度在相机之后。

由 camera/tof 的 quat≈`(0.707, 0, 0.707, 0)`（绕 Y≈+90°）与嘴尖更负的 z 可推断：头壳父系里 **−Z 大致朝脸外（前）**；IMU site **单位四元数** = 敏感轴对齐该 CAD 父系，**不是**相机光轴系。

### 6.2 板级朝向（18×14 可行姿态）

控制环**不读**头 IMU，无 `duck-control` mount 契约。推荐先定一种，丝印画清芯片 +X/+Y/+Z，软件再映射。

| 姿态 | 板怎么装 | 芯片顶（+Z） | 适用 |
|------|----------|--------------|------|
| **H1 推荐** | 板面近似平行于脸平面，元件面朝**颅腔内侧**（背对脸壳） | 大致沿头壳 **+Z**（向后/向内） | 厚度方向最省；线从 J1 向下/向颈接 Qwiic |
| **H2** | 同上，元件面朝脸 | +Z 朝前（−Z_head） | 亦可；注意外壳干涉 |
| **H3** | 竖板，元件面朝左或右 | +Z 朝 ±Y | 仅当 H1/H2 装不下 |

**连接器：** J1 朝向**颈/躯干侧**出线（便于 STEMMA 下到 HAT），勿朝向嘴尖挡相机/ToF。

**芯片旋转（在选定姿态下）：** 任选 0/90/180/270°，但丝印必须标 Pin1 与 +X/+Y；首版建议芯片 **+X 沿板长边、+Y 沿板短边**，与板框平行，便于以后改 mount 矩阵。

与机身对照：机身有强制 `trunk=[+z,+y,−x]`；头部**无强制**，以结构能装下 + 标定为准。

## 7. 与机身板对照

| | 机身 [[imu-to-dxl-ref-schematic]] | **本板** |
|--|-----------------------------------|----------|
| 总线 | DXL TTL 从机 | I²C 从机 |
| MCU | 有 STM32 | **无** |
| 电源 | VBATT→3V3 LDO | 直取 3V3 |
| 尺寸 | ~25×17 | **18×14** |
| 控制环 | 用 | **不用** |

相关：[[board-imu-head]] · [[head-imu-ref-bom]] · [[dual-imu-board-selection]] · [[elec-rpi-robot-hat]] · [[vl53-tof]]
