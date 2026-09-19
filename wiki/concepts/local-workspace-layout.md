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
> 根：`D:\projects\microduck` —— **根就是基础工程（`ScrapMeta/microduck-diy`）的工作树**（治理 §10）。

## 本仓（自有 · 受版本控制）

| 目录 | 作用 |
|------|------|
| `governance/` | 治理细则 + 通用模板 + `upstreams.lock`（**入仓**） |
| `wiki/` | **llm-wiki** 规格与资料真源 |
| `imu_to_dxl/` | 机身 IMU v0.3 · 板设计 + 固件 |
| `image/` | Zero 3W **seed 镜像**构建脚本与 overlay（`out/*.img*` 不入库） |
| `cad/` | 耐久 `.3mf` |
| `scripts/` | 台架 / 上机脚本（`dxl_ping.py`） |
| `.cursor/rules/` | 职能 rule（**入仓**，与治理同受版本控制） |
| `AGENTS.md` | **Agent 治理入口**（不变量 + 指向 `governance/`） |

## 自有兄弟仓与本地临时（ignore）

| 目录 | 作用 |
|------|------|
| `microduck_ros2/` | ROS2 并行移植（**自有仓** · 独立 push）· 见 [[ros2-migration-plan]] |
| `temp/` `vms/` `.tmp/` `.venv-cad/` | 本地临时，**非真源** |

## 只读参考克隆 `refs/`（ignore）

| 目录 | 作用 |
|------|------|
| `refs/microduck/` | 真机运行时（robotd） |
| `refs/microduck_rl/` | 训练 / MJCF / 网格真源 |
| `refs/elec_RPI_Robot_HAT/` | 官方 HAT KiCad |
| `refs/microduck-simulator/` | HuggingFace Space 仿真 |
| `refs/microduck-replica/` | 复刻电控对照 |
| `refs/microduck_app/` · `refs/microduck_kinematics_rs/` · `refs/microduck_maploc_rs/` · `refs/microduck_pet_detect/` · `refs/microduck_sounds/` | apirrone 分件仓 |
| `refs/OpenMicroDuck/` | 社区原型参考 |
| `refs/Microduck-build-tutorial/` | 外部只读 · AI-FanGe 中文教程仓（旁路，非主线）· 见 [[aifange-microduck-build-tutorial]] |
| `refs/OpenRB-150/` | ROBOTIS 开源舵机控制板（Arduino SAMD 板级包，Apache-2.0） |

CAD 网格真源：`refs/microduck_rl/.../robot/microduck/`；审阅 3MF 输出：`cad/`。

旁路调研页见 [`_archive/`](../_archive/README.md)。

## 路径写法约定

- **本仓内**：从根写（`governance/…` · `wiki/…` · `cad/…`）——**不再**加 `microduck-diy/` 前缀
- **只读参考**：写 `refs/<clone>/…`（例：`refs/microduck/scripts/setup-board.sh`）
- **只引仓库名时**（如「官方 `microduck_rl` 是 MJCF 真源」）→ **不加** `refs/`：那是仓名，不是本地路径
- 版本锁定：`governance/upstreams.lock`，用 `governance/refresh-upstreams.ps1 -Fetch` 重生成
 （**不带 `-Fetch` 就不联网**，`Behind` 只是上次 fetch 的快照；`Behind=0` 不等于「已最新」）

> **交付物归属**：根（本仓）与 `microduck_ros2/` 是自有仓；`refs/` 内只读，
> 不在其中留未提交改动（治理 §11）。
> **禁用 `git clean -x`**：它会删除被 ignore 的 `refs/`（治理 §10.4）。

相关：[[microduck-diy]] · [[ros2-migration-plan]] · [[SCHEMA]]
