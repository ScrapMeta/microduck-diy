---
title: 本地工作区布局
created: 2026-08-30
updated: 2026-09-19
type: concept
tags: [workspace, open-source, diy]
sources: []
confidence: high
related: [microduck-diy, microduck, opensource-coverage, ros2-migration-plan]
---

# 本地工作区布局

> **布局真源** —— 全树以本页为准；[`AGENTS.md`](../../AGENTS.md) 只列规则，不重复布局。
> 根：`D:\projects\microduck` —— **根就是本仓（`ScrapMeta/microduck-diy`）的工作树**。

## 本仓（自有 · 受版本控制）

| 目录 | 作用 |
|------|------|
| `AGENTS.md` | **唯一规则源**（红线 · 改法表 · 记录约定 · 角色表） |
| `README.md` | 给人看的导航 |
| `wiki/` | **规格与资料真源**（导航 → [[index]]；欠什么 → [[tasks]]；流水 → [[log]]） |
| `.cursor/skills/<role>/SKILL.md` | **角色操作手册**（pm · hardware · software · structure）—— 入仓 |
| `scripts/` | 台架 / 上机脚本 ＋ 两台 linter ＋ `upstreams.lock` |
| `imu_to_dxl/` | 机身 IMU v0.3 · 板设计 + 固件 |
| `image/` | Zero 3W **seed 镜像**构建脚本与 overlay（`out/*.img*` 不入库） |
| `cad/` | 耐久 `.3mf` |
| `.github/workflows/ci.yml` | push `main` 跑两台 linter（防漂移） |

## 自有兄弟仓与本地临时（ignore）

| 目录 | 作用 |
|------|------|
| `microduck_ros2/` | ROS2 并行移植（**自有仓** · 独立 push）· 见 [[ros2-migration-plan]] |
| `temp/` `vms/` `.tmp/` `.venv-cad/` `res/` | 本地临时，**非真源** |

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

旁路调研页见 [`_archive/`](../_archive/README.md)；**2026-09-19 停用的旧治理层**在 [`_archive/governance/`](../_archive/governance/README.md)。

## 路径写法约定

- **本仓内**：从根写（`wiki/…` · `cad/…` · `scripts/…`）——**不加** `microduck-diy/` 前缀
- **只读参考**：写 `refs/<clone>/…`（例：`refs/microduck/scripts/setup-board.sh`）
- **只引仓库名时**（如「官方 `microduck_rl` 是 MJCF 真源」）→ **不加** `refs/`：那是仓名，不是本地路径
- 版本锁定：`scripts/upstreams.lock`，用 `scripts/refresh-upstreams.ps1 -Fetch` 重生成
 （**不带 `-Fetch` 就不联网**，`Behind` 只是上次 fetch 的快照；`Behind=0` 不等于「已最新」）

> **交付物归属**：根（本仓）与 `microduck_ros2/` 是自有仓；`refs/` 内只读，
> 不在其中留未提交改动。**交付物必须落在自己有 push 权限的仓里。**
> **禁用 `git clean -x`**：它会删除被 ignore 的 `refs/`。

相关：[[microduck-diy]] · [[ros2-migration-plan]] · [[index]] · [[tasks]]
