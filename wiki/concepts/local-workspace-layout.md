---
title: 本地工作区布局
created: 2026-08-30
updated: 2026-09-16
type: concept
tags: [workspace, open-source, diy]
sources: []
confidence: high
related: [microduck-diy, microduck, opensource-coverage, ros2-migration-plan]
---

# 本地工作区布局

> **布局真源**：治理细则 §1.3 只列治理相关子集，全树以本页为准。
> 根：`D:\projects\microduck`

## 本 diy 相关

| 目录 | 作用 |
|------|------|
| `microduck-diy/` | **GitHub 基础工程**（[[microduck-diy]]）· Issue / Milestone |
| `microduck-diy/governance/` | 治理细则 + 通用模板 + `upstreams.lock`（**入仓，受版本控制**） |
| `microduck-diy/wiki/` | **llm-wiki** 规格与资料真源 |
| `microduck-diy/imu_to_dxl/` | 机身 IMU v0.3 · 板设计 + 固件 |
| `microduck-diy/image/` | Zero 3W **seed 镜像**构建脚本与 overlay（`out/*.img*` 不入库） |
| `microduck-diy/cad/` | 耐久 `.3mf` |
| `AGENTS.md` | 治理**转发存根**（工作区根，不是仓）——不变量 + 指向 `governance/` |
| `microduck_ros2/` | ROS2 并行移植（**自有仓** · software 范畴）· 见 [[ros2-migration-plan]] |
| `handoffs/` | **已废止**（仅存去向索引）· 见 [handoffs/README](../../../handoffs/README.md) |
| `temp/` / `vms/` | 本地临时，**非真源** |
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

> **交付物归属**：只有 `microduck-diy/` 与 `microduck_ros2/` 是自有仓；其余克隆只读，
> 不在其中留未提交改动（治理 §11）。

相关：[[microduck-diy]] · [[ros2-migration-plan]] · [[SCHEMA]]
