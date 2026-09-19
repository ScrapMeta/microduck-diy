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

## 宿主工具链（Windows · 2026-09-19 实况）

本仓脚本在两处跑：**开发机（Windows）** 与 **CI（ubuntu ＋ Python 3.12）**。开发机这边的坑：

| 项 | 实况 | 对 agent 的影响 |
|----|------|-----------------|
| **Git** | 2.31.1 → **2.55.0.3**（2026-09-19 升级） | 升级前 **任何 `git commit` 都失败**：Cursor 会注入 `git commit --trailer "Co-authored-by: Cursor …"`，而 `--trailer` 是 **git 2.32+** 才有 → `unknown option 'trailer'`（连 `--dry-run` 都炸）。应急是**用全路径 `C:\Program Files\Git\cmd\git.exe` 调用**绕开改写；现已根治 |
| **`python`** | → `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`（**3.12.10**） | 升级前它解析到 **hermes agent 的 venv（3.11.15）**，**不是**系统 Python。3.12 的 PATH 条目必须排在 hermes **之前** |
| **`python3`** | 仍是 **Microsoft Store 占位符**（`…\WindowsApps\python3.exe`）→ 报 not found | 脚本里的 `python3` 在开发机上**不可直接用**；要修得去「设置 → 应用 → 应用执行别名」**关掉** `python3.exe`（GUI，agent 改不了） |
| **`py`** | 可用（默认 **3.12**）· `py -3.9` **坏**（注册表指向不存在的 `C:\Python39`） | 别拿 `py -3` 当通用入口 |
| **PATH 顺序** | **机器 PATH 整体在用户 PATH 之前** | 要抢回 `python`，光丢进用户 PATH 尾部没用 |
| **残留** | 机器 PATH 有两条死路径 `C:\Python\Python38\Scripts;` `C:\Python\Python38;`，而该目录**已无 `python.exe`**（只剩孤立 `site-packages`） | 那批坏 `Scripts\*.exe` 抢在真货之前解析 `tensorboard` / `huggingface-cli` / `modelscope`，**执行即静默失败** |

**脚本版本下限 = Python 3.9**：`scripts/` 下四个脚本**只用 stdlib**，唯一的新语法是 `str.removeprefix`。
实测 **3.9.7 与 3.12.10** 上 `wiki_lint` / `refs_lint` 均 **0 error**。
**别引入 `pyserial` 之类的硬依赖** —— 开发机与板子都不保证有（理由见 `scripts/README.md`）。

**uv 只管项目级 venv**（`%APPDATA%\uv\python\` 有 3.11.15 / 3.12.13），**不占任何全局名字** ——
`python` / `python3` / `py` 这三个入口**uv 修不了**，只能靠注册过的系统安装。
本仓现场：`.venv-cad`（3.11 ＋ cadgen 0.5.0）· `refs/microduck_rl/.venv`（3.12）。

> ⚠️ **agent 会话的 PATH 是启动时快照** —— 改完 PATH **要新开终端**才生效。
> 未清项（`C:\Python\Python38` · `C:\Python\Python39` · 两条死 PATH · 商店别名）见 [[tasks]]。

## 路径写法约定

- **本仓内**：从根写（`wiki/…` · `cad/…` · `scripts/…`）——**不加** `microduck-diy/` 前缀
- **只读参考**：写 `refs/<clone>/…`（例：`refs/microduck/scripts/setup-board.sh`）
- **只引仓库名时**（如「官方 `microduck_rl` 是 MJCF 真源」）→ **不加** `refs/`：那是仓名，不是本地路径
- 版本锁定：`scripts/upstreams.lock`，用 `scripts/refresh-upstreams.ps1 -Fetch` 重生成
 （**不带 `-Fetch` 就不联网**，`Behind` 只是上次 fetch 的快照；`Behind=0` 不等于「已最新」）

> **交付物归属**与 **`refs/` 只读** · **禁用 `git clean -x`** 是红线，
> 正文只在 [`AGENTS.md`](../../AGENTS.md)（「红线」「仓库形态」）；本页只管**路径怎么写**。

相关：[[microduck-diy]] · [[ros2-migration-plan]] · [[index]] · [[tasks]]
