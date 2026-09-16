---
title: imu_to_dxl v2
created: 2026-08-30
updated: 2026-09-07
type: entity
tags: [board, imu, firmware]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - ../refs/microduck_rl/src/mjlab_microduck/robot/microduck/robot_walk.xml
confidence: medium
related: [board-imu-to-dxl, elec-three-boards, board-interconnect, elec-rpi-robot-hat, opensource-coverage, mechanical-bom-rl, local-workspace-layout]
---

# imu_to_dxl v2

机身 IMU 子板：芯片 **LSM6DSV16X**（片上 SFLP 四元数），挂在 Dynamixel 总线 **ID 200**，Protocol 2.0 @ 1 Mbps。

> **DIY 参考板速查：** [[board-imu-to-dxl]] · 三板 [[elec-three-boards]]  
> **外形口径：** DIY 实布 **32×22**（v0.3 · [[board-imu-to-dxl]]）；下表 placeholder **22×16×4** 仅 Viewer 仿真壳。

## 开源状态

- **原理图 / 固件 / KiCad / PCB 网格均未公开**
- 旧 `microduck_runtime` 有 `flash.sh`（仓已下架）
- 产线烧录；**不进 OTA**

## 结构里能确认的（无板外形）

公开 MJCF **无** `imu*.stl`。仅有传感器 **site**：

| site | 父连杆 | 相对父系约 (mm) | 含义 |
|------|--------|-----------------|------|
| `imu` | `trunk_base` | **(-21, 0.07, -14.7)** | 机身控制 IMU（本板） |
| `head_imu` | 头内（RL：`jaw_soft`） | ~(15, 0.1, -51) | 头部 IMU，非本板 |
| `imu_bno` | `trunk_base`（仅 app alpha） | ~(-32, 14, 43) | HAT BMI088；RL 控制不用 |

零位世界系下 `imu` 约 **(-21, 0.07, 105) mm**（含 trunk 抬高）。附近网格：`power_support`、`banana_pcb_locker`、壳、电池包络等。

**板长宽厚 / 孔距：结构中无法得到。**

## Viewer 占位

CAD Viewer 能力边界：**GLB/STL 无零件树且易发黑**；**URDF 有颜色、可按 link 点选，但侧栏只有 Joints**；**装配树只有 STEP**。

**工具约定：** Cursor 全局 text-to-cad **0.5**。网格真源：`refs/microduck_rl/.../robot/microduck/`；审阅产物：`cad/`（仅 3MF）。

占位 link（若用 URDF 审阅）：

| link 名 | 含义 | 约尺寸 mm | URDF 色 |
|---------|------|-----------|---------|
| `imu_to_dxl_placeholder` | 机身 site `imu` | 22×16×4 | 青 |
| `head_imu_placeholder` | 头 site `head_imu` | 18×14×3 | 粉 |

DIY 参考板（非官方）：[[board-imu-to-dxl]] · 摆放细页 [[imu-to-dxl-ref-pcb-layout]]。

相关：[[board-imu-to-dxl]] · [[elec-three-boards]] · [[board-interconnect]] · [[elec-rpi-robot-hat]] · [[local-workspace-layout]]
