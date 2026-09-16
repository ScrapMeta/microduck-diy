---
title: AI-FanGe Microduck-build-tutorial
created: 2026-09-09
updated: 2026-09-16
type: entity
tags: [external, diy, reference, mechanical]
sources:
  - https://github.com/AI-FanGe/Microduck-build-tutorial
  - handoffs/README.md（原 2026-09-09 pm→pm/sw/hw/structure 评估工单已清理）
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

俗称「中文改良版 Microduck」。公开仓：[AI-FanGe/Microduck-build-tutorial](https://github.com/AI-FanGe/Microduck-build-tutorial)；`AI-FanGe/Microduck` 链接 **404**。

| 项 | 值 |
|----|-----|
| 本地（只读） | `D:\projects\microduck\Microduck-build-tutorial` |
| 复核 HEAD（2026-09-15） | `4967821` · `main` = `origin/main`（已 fetch，无落后） |
| 评估时 HEAD（2026-09-09） | `9a11a40` |

## 定位

MarcDcls/microduck（microban 系）的中文教程封装：Pi Zero 2 W + OpenRB-150 + BNO08x + XL330，Python 环 + 手柄驱动 `walk.onnx`。**不是** Pollen 官方栈中文版。

## 对本 diy

**旁路参考，非主线。**（pm 总评 2026-09-09 维持；2026-09-15 对照上游增量后 **结论不变**。）

| 做 | 不做 |
|----|------|
| 旁路借鉴：装机文档结构、EH 线束工艺、手柄/镜像/过流**思路**（自写） | 主线 BOM 写入 OpenRB / Pi Zero / BNO 替代 200 / ID 1–14 / 其整套结构件 |
| 通用件：XL330、EH 3P 等按官方/diy 清单 | 为「兼容该仓」改 imu-to-dxl v0.3 或 diy cad 定稿 |

历史评估链（**handoff 已废止**，2026-09-16 正文已清理）：去向索引见 [handoffs/README.md](../../../../handoffs/README.md)。

## 上游增量（`9a11a40` → `4967821`）

自评估后上游仅删除大体积资产，**未改** OpenRB / Pi / BNO / 6 V / ID 1–14 主故事：

| 提交 | 变更 |
|------|------|
| `34656ce` | 删除 `mjlab_microduck/.../robot`（仿真网格资源） |
| `570e0c2` | 删除整棵 `microduck/cad/`（STEP/STL） |
| `4967821` | 删除 `microduck/docs/`（旧装机/BOM 子文档） |

现行打印物：仓库根 **`microduck3D打印.3mf`**（约 5.3 MB）。根 README BOM 仍写「使用 `microduck/cad/`」——**路径已失效**，以 3mf / 仓库实际文件为准。`docs/assets/`（爆炸图等）仍在。

## 硬件视角

| 项 | 该仓（README 现行） | diy 主线 |
|----|---------------------|----------|
| 主控 / 桥 | Pi Zero 2W · **OpenRB-150 USB** | Radxa · **HAT TTL** |
| 机身 IMU | BNO08x **I²C** | **`imu_to_dxl` ID 200** |
| 电池 | 成品 **~6 V**（Pi 另 5 V，共地） | **NP-F** → HAT（互联定稿；#9 不采用 DXL 回灌） |
| DXL 座 | EH 3P（同族） | B3B-EH · J13/J14 |

- **可借鉴：** EH 压接/改线长、线序与共地检查。  
- **禁止混 BOM：** OpenRB、Pi Zero 默认主控、BNO 替代 200、6 V 唯一电池故事、ID 1–14、OpenRB 与 HAT 并接同链。  
- **制板/订单：无阻塞。**

## 软件视角

| 项 | 该仓 | 官方 / diy |
|----|------|------------|
| 环 | Python 50 Hz | Rust `robotd` 50 Hz |
| IMU | BNO08x I²C | `imu_to_dxl` ID 200 |
| ID | 1–14（嘴可选 15，行走不依赖） | 10–14 / 20–24 / 30–34（+嘴） |
| 策略 | `walk.onnx`；观测按 14 DOF 组装（基线 **51→14** 量级，非官方 61） | **61→14**（cmd13） |

- **可借鉴：** 无头手柄服务、镜像分层、过流思路（自写，勿拷 GPL）。  
- **禁止照搬：** ID 图、BNO 主路径、51 维契约、Python 主环当量产权威。  
- **对 `imu_to_dxl` / `robotd`：无直接代码复用。**

## 结构视角

| 项 | 该仓（现行） | 官方 / diy |
|----|--------------|------------|
| 可打印交付 | 根目录 **`.3mf` 包**；仓内 STEP/STL **已删** | `microduck-diy/cad/` + RL 网格对照 |
| 谱系 | Marc / microban（历史 CAD 已不在树内） | Pollen |
| 手臂 / 命名 | 评估时有臂、与官方件名 **0 交集** | 无臂；`trunk_base` 等 |

- **可借鉴：** 装机文档结构、线束/打印纪律（见历史 structure 评估）。  
- **禁止当主线模具：** 其 3mf/历史 CAD、带臂 DOF、旧舱体供电几何。  
- **diy cad：无阻塞。**

相关：[[microduck-diy]] · [[openmicroduck]] · [[board-imu-to-dxl]] · [[board-interconnect]] · [[board-hat]] · [[print-bom-rl]] · [[local-workspace-layout]]
