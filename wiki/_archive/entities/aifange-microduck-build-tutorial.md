---
title: AI-FanGe Microduck-build-tutorial
created: 2026-09-09
updated: 2026-09-09
type: entity
tags: [external, diy, reference, mechanical]
sources:
  - ../handoffs/2026-09-09-pm-to-pm-aifange-microduck.md
  - ../handoffs/2026-09-09-pm-to-software-aifange-sw-eval.md
  - ../handoffs/2026-09-09-pm-to-hardware-aifange-hw-eval.md
  - ../handoffs/2026-09-09-pm-to-structure-aifange-mech-eval.md
confidence: high
related:
  - microduck-diy
  - openmicroduck
  - local-workspace-layout
  - board-imu-to-dxl
  - board-interconnect
  - board-hat
  - print-bom-rl
  - mechanical-bom-rl
---

# AI-FanGe · Microduck-build-tutorial

俗称「中文改良版 Microduck」。公开仓是 [AI-FanGe/Microduck-build-tutorial](https://github.com/AI-FanGe/Microduck-build-tutorial)；`AI-FanGe/Microduck` 链接 **404**。

本地：`D:\projects\microduck\Microduck-build-tutorial`（外部只读）。

## 定位

MarcDcls/microduck（microban 系）的中文教程封装：Pi Zero 2 W + OpenRB-150 + BNO08x + XL330，Python 环 + 手柄驱动 `walk.onnx`。**不是** Pollen 官方栈中文版。

## 对本 diy

**旁路参考，非主线。**（pm 总评 2026-09-09 维持；三职能评估均 done。）

| 做 | 不做 |
|----|------|
| 旁路借鉴：装机文档结构、EH 线束工艺、手柄/镜像/过流**思路**（自写） | 主线 BOM 写入 OpenRB / Pi Zero / BNO 替代 200 / ID 1–14 / 其整套 CAD |
| 通用件：XL330、EH 3P 等按官方/diy 清单 | 为「兼容该仓」改 imu-to-dxl v0.3 或 diy cad 定稿 |

详单：`handoffs/2026-09-09-pm-to-pm-aifange-microduck.md` §pm 总评 · sw/hw/structure 各 handoff。

## 硬件视角（2026-09-09）

来源：`handoffs/2026-09-09-pm-to-hardware-aifange-hw-eval.md`（done）。**未改** imu-to-dxl v0.3 / 三板互联。

| 项 | 该仓（README 现行） | diy 主线 |
|----|---------------------|----------|
| 主控 / 桥 | Pi Zero 2W · **OpenRB-150 USB** | Radxa · **HAT TTL** |
| 机身 IMU | BNO08x **I²C** | **`imu_to_dxl` ID 200** |
| 电池 | 成品 **~6 V**（Pi 另 5 V，共地） | **NP-F** → HAT 5–28 V |
| DXL 座 | EH 3P（同族） | B3B-EH · J13/J14 |

- **可借鉴：** EH 压接/改线长、线序与共地检查。  
- **禁止混 BOM：** OpenRB、Pi Zero 默认主控、BNO 替代 200、6 V 唯一电池故事、ID 1–14、OpenRB 与 HAT 并接同链。  
- **制板/订单：无阻塞。**  
- 注意：内嵌 `docs/bom.md` 仍写旧 HAT+18650，与根 README 不一致——以 README 为准。

## 软件视角（2026-09-09）

来源：`handoffs/2026-09-09-pm-to-software-aifange-sw-eval.md`（done）。本地 HEAD `9a11a40`。

| 项 | 该仓 | 官方 / diy |
|----|------|------------|
| 环 | Python 50 Hz | Rust `robotd` 50 Hz |
| IMU | BNO08x I²C | `imu_to_dxl` ID 200 |
| ID | 1–14（无嘴） | 10–14 / 20–24 / 30–34（+嘴） |
| 策略 | `walk.onnx` **51→14**（cmd3） | **61→14**（cmd13） |

- **可借鉴：** 无头手柄服务、镜像分层、过流/电流代理思路（自写，勿拷 GPL）。
- **禁止照搬：** ID 图、BNO 主路径、51 维契约、Python 主环当量产权威。
- **对 `imu_to_dxl` / `robotd`：无直接代码复用。**

## 结构视角（2026-09-09）

来源：`handoffs/2026-09-09-pm-to-structure-aifange-mech-eval.md`（done）。**未改** `microduck-diy/cad/` / day*。

| 项 | 该仓 `microduck/cad/` | 官方 / diy（RL STL） |
|----|------------------------|----------------------|
| 谱系 | Marc / microban；Onshape `d424992a…` | Pollen；`80492769…` |
| 手臂 | **有**（肩/肱/尺 + 轴承座） | **无** |
| 打印件名 | `pelvis`/`chest`/`trunk_top`/… | `trunk_base`/`left_shell`/`power_support`/… |
| 与官方名交集 | **0** | — |
| 舱体叙事 | 旧文档 Pi+HAT@躯干顶；README 现行 OpenRB+BNO（CAD 未重画） | 头舱 Radxa+HAT；背板 NP-F + `imu_to_dxl` |

- **可借鉴：** 轴承件打印朝向、双电机块先布线再入槽、EH 改线长、脚底增摩、PLA 近焊纪律；装机文档目录结构。
- **禁止当主线模具：** 整套 STEP/STL/3MF、带臂 DOF、`board_spacer`/trunk_top 支架、18650/6V 内仓几何。
- **diy cad：无阻塞。** 内嵌 `mjlab_…/assets` 官方同名网格仅仿真用，≠ 可打印 CAD。

相关：[[microduck-diy]] · [[openmicroduck]] · [[board-imu-to-dxl]] · [[board-interconnect]] · [[board-hat]] · [[print-bom-rl]]
