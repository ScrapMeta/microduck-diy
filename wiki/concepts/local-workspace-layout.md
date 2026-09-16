---
title: 本地工作区布局
created: 2026-08-30
updated: 2026-09-15
type: concept
tags: [workspace, open-source, diy]
sources: []
confidence: high
related: [microduck-diy, microduck, opensource-coverage]
---

# 本地工作区布局

根：`D:\projects\microduck`

## 本 diy 相关

| 目录 | 作用 |
|------|------|
| `microduck-diy/` | **GitHub 基础工程**（[[microduck-diy]]）· Issue / Milestone |
| `microduck-diy/imu_to_dxl/` | 机身 IMU v0.3 + 固件 |
| `microduck-diy/wiki/` | **llm-wiki** 规格与资料真源 |
| `microduck-diy/cad/` | 耐久 `.3mf` |
| `AGENTS.md` / `docs/` | Agent 治理 v0.8 入口与细则（工作区根） |
| `handoffs/` | **已废止**（存量只读） |
| `Microduck-build-tutorial/` | 外部只读 · AI-FanGe 中文教程仓（旁路，非主线）· 见 [[aifange-microduck-build-tutorial]] |

## 官方引用（只读）

| 目录 | 作用 |
|------|------|
| `microduck/` | 真机运行时 |
| `microduck_rl/` | 训练 / MJCF / 网格真源 |
| `elec_RPI_Robot_HAT/` | 官方 HAT KiCad |
| `OpenRB-150/` | ROBOTIS 开源舵机控制板（Arduino SAMD 板级包，Apache-2.0） |

CAD 网格真源：`microduck_rl/.../robot/microduck/`；审阅 3MF 输出：`microduck-diy/cad/`。

旁路调研页见 [`_archive/`](../_archive/README.md)。

相关：[[microduck-diy]] · [[SCHEMA]]
