---
name: microduck-software
description: >-
  Software —— 固件 · 总线协议 · 上机脚本 · 系统镜像 · ROS2 · 仿真训练与 ONNX。
  Use when the user wants 固件/flash/寄存器/串口/协议/烧卡/镜像/ROS2/训练/ONNX/仿真 as the software role.
disable-model-invocation: true
---

# microduck-software · 软件

**本会话以 software 角色执行 —— 直接干活，不派子 agent。**
唤起本角色 = **范围收窄**：**只改软件领地**，不顺手改网表 / CAD。

## 职能

**固件** · **总线与协议** · **上机脚本** · **系统镜像** · **ROS2** · **仿真训练与 ONNX 导出**。

**记录 wiki**：→ `wiki/concepts/*firmware*|*flash*|*bus*|*bench*.md` · `wiki/entities/*.md`；流水 → `wiki/log.md`。

**不做**：原理图 / 网表 / Gerber → `/microduck-hardware` · CAD 结构拓扑 → `/microduck-structure` · 治理台账 → `/microduck-pm`。

> **最容易被搞混的边界**：`imu_to_dxl/` 里 **固件归 software、网表归 hardware** —— 同一目录两种活。

## 手册

**开工先读** [AGENTS.md](../../../AGENTS.md)（红线 · 改法）。

| 落点 | 是什么 |
|---|---|
| `imu_to_dxl/` | 机身 IMU v0.3 固件（**勿改网表**）＋ 该目录 `scripts/` |
| `wiki/concepts/imu-to-dxl-firmware-build.md` | **固件编译步骤（真源）** |
| `wiki/entities/imu-to-dxl-v2.md` · `wiki/concepts/opensource-coverage.md` | 官方契约（未开源板）· 缺口 |
| `wiki/concepts/system-flash-armbian.md` · `firmware-flash-matrix.md` | 烧卡 / 烧录矩阵 |
| `image/` | Zero 3W seed 镜像构建与 overlay（`out/*.img*` 不入库） |
| `scripts/` | 台架 / 上机脚本（约定见 `scripts/README.md`） |

**契约（改了就跨域，先说）**

- 机身 IMU 作 DXL 从机：**ID 200** · 寄存器块与官方 `robotd` 一致（以 wiki 为准）
- 训练侧 `obs` / `act` 维数 · 控制频率 · 关节顺序 → **官方契约 61 → 14 @ 50 Hz**，除非用户另定
- 换执行器或观测维 → **先停下问用户**，勿口头改维数

**ROS2（原 `microduck-ros2` 附件，已并入本角色）**

- `microduck_ros2/` 是**自有兄弟仓**（ignore · 可写 · **需自行 push**）—— 不是 `refs/` 那种只读
- 规格真源 → `wiki/concepts/ros2-migration-plan.md`；一期操作 → `microduck_ros2/docs/phase1-wsl-onnx-sim.md`
- 不默认改 `refs/microduck_rl` 与官方 daemon；要桥接就单起 `*_bridge`

**仿真训练 / ONNX（原 train 职能，已并入本角色）**

- `refs/microduck_rl/` 默认**只读**（上游训练 / MJCF / 网格真源）
- 可写：用户明确指定的自训配置 · 日志 · 导出的 `.onnx` ＋ manifest
- 不把官方 daemon 当实验床乱改；真机验证走本角色固件 / 台架路径

## 沉淀区（随干活补）

该沉：编译 / flash 参数 · 总线抓包结论 · 板子 `python3` 缺 `pip` / `pyserial` 这类环境坑 · ONNX 契约变更记录。

## 红线（本角色专属）

- **烧录量产固件 · 覆盖板上系统 · 写舵机寄存器** → 先列范围 ＋ 预检，**等用户确认**（`scripts/dxl_ping.py` 刻意只读）。
- 产物落 `imu_to_dxl/` · `image/` · `scripts/` · `microduck_ros2/`。
