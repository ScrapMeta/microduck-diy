---
title: imu_to_dxl 参考 PCB 摆放
created: 2026-09-03
updated: 2026-09-09
type: concept
tags: [imu, board, jlceda]
confidence: high
related:
  - board-imu-to-dxl
  - elec-three-boards
  - imu-to-dxl-ref-schematic
  - imu-to-dxl-ref-chip-wiring
  - imu-to-dxl-ref-bom
  - imu-to-dxl-v2
  - dual-imu-board-selection
---

# imu_to_dxl 参考 PCB 摆放

> **REFERENCE — NOT OFFICIAL**  
> **现行：`imu-to-dxl v0.3`（2026-09-09）· 1 号大板 32×22。**
> 总览：[[board-imu-to-dxl]] · BOM：[[imu-to-dxl-ref-bom]] · 接线：[[board-interconnect]]

## v0.3 定稿（相对 v0.2）

| 项 | 说明 |
|----|------|
| 板框 | **32 × 22 mm**；四角 φ2.2；孔距 **29 × 19** |
| DXL | **J1 进 + J3 出**（双 B3B-EH）；`VBATT` J1↔J3 ≥40 mil 或铺铜 |
| 调试 | **J2 BM07 7P**：3V3 · CLK · DIO · GND · TX · RX · RST |
| 保护 | 座侧 `DXL_BUS`：D1 TVS + D2 5.1 V；R6→芯片侧 `DXL_DATA` |
| 电源 | U3+C4/C5 可贴 **J3 侧**；C5 贴 U3 VIN；C2 贴 VOUT；+C6 on 3V3 |
| 上拉 | R2→U1 CS；R1/R3/R4/R5→MCU 侧 |
| 丝印 | 板名 `imu-to-dxl v0.3`；U1 轴 +X/+Y/+Z；J2 缩写见 BOM |

布局示意 SVG：[`imu-to-dxl-board1-32x22-placement.svg`](../assets/pcb/imu-to-dxl-board1-32x22-placement.svg)

```
Y=22  ○──── J2 BM07 7P ────○
      │  U2     ★U1 LSM6    │
      │  U6 R6 D1/D2  U3    │
Y=0   ○── J1 EH ── J3 EH ──○
```

## 历史 · v0.2（2026-09-05）

丝印 `imu-to-dxl v0.2` · ~25×17 · 单 EH · BM04 4P SWD。

| 图 | 文件 |
|----|------|
| PCB | [`imu-to-dxl-v0.2-pcb-2026-09-05.png`](../assets/pcb/imu-to-dxl-v0.2-pcb-2026-09-05.png) |
| 3D | [`imu-to-dxl-v0.2-3d-2026-09-05.png`](../assets/pcb/imu-to-dxl-v0.2-3d-2026-09-05.png) |

## 历史 · v0.1（2026-09-04）

`imu-to-dxl-v0.1-{sch,pcb,3d,3d-top}-2026-09-04.png`

相关：[[board-imu-to-dxl]] · [[imu-to-dxl-ref-schematic]] · [[imu-to-dxl-ref-bom]] · [[imu-to-dxl-v2]]
