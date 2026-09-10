---
title: 本地工作区布局
created: 2026-08-30
updated: 2026-09-10
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
| `microduck-diy/` | 工程仓（[[microduck-diy]]） |
| `microduck-diy/imu_to_dxl/` | 机身 IMU v0.3 + 固件 |
| `microduck-diy/wiki/` | **本知识库** |
| `microduck-diy/cad/` | 耐久 `.3mf` |
| `docs/` | Agent 治理（工作区根） |
| `handoffs/` | 跨 agent 工单（工作区根） |

## 官方引用（只读）

| 目录 | 作用 |
|------|------|
| `microduck/` | 真机运行时 |
| `microduck_rl/` | 训练 / MJCF / 网格真源 |
| `elec_RPI_Robot_HAT/` | 官方 HAT KiCad |

CAD 网格真源：`microduck_rl/.../robot/microduck/`；审阅 3MF 输出：`microduck-diy/cad/`。

旁路调研页见 [`_archive/`](../_archive/README.md)。

相关：[[microduck-diy]] · [[SCHEMA]]
