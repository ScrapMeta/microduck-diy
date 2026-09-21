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

## 板级诊断（U2D2 · 主控）—— 2026-09-21 实做

**判据真源** → `wiki/concepts/imu-to-dxl-firmware-triage.md`（`@136` status 位表 · 「静默零块」坑 · 逐块结果）。
本节只说**怎么跑**；台架供电 / 限流纪律 → `/microduck-hardware`（`wiki/concepts/dxl-bench-method.md` · `wiki/concepts/hat-dxl-bus-debug.md`）。

### A. 台架 · U2D2 逐块分诊 IMU 板

```bash
# 开发机（Windows）：pyserial 是硬前提 —— stdlib 回退是 Linux 专有
uv run --with pyserial python scripts/dxl_ping.py scan --port COM7 --baud 1000000,57600
```

扫到 **model `10200`** 只证明 **DXL 从机在跑**，**不证明 IMU 有数** —— 必须再读两块：

| 块 | 地址 · 长度 | 判据 |
|----|------------|------|
| 数据块 | `124` · 12 B | **全 0 = SFLP 没出数**（Ping 照答，静默失败） |
| 诊断块 | `136` · 8 B | `u16` counter **递增**？`u8` status **`0x03`** = 活 |

```bash
uv run --with pyserial python scripts/dxl_ping.py read --port COM7 --id 200 --addr 124 --length 12
uv run --with pyserial python scripts/dxl_ping.py read --port COM7 --id 200 --addr 136 --length 8
```

一句话判板：**`0x03` ＋ counter 走 = 可用** · **`0x00` = DXL 活但 IMU 芯片 / SPI 死** · **完全无应答 = MCU 侧**（SWD 也认不到）。
**别用 `info --id 200`** —— 它按 XL330 表读**地址 6**，本板固件版本在**地址 2**（`imu_to_dxl/firmware/src/control_table.c`）。

### B. 主控 · 远程验 IMU ＋ 腿

```bash
scp -i <私钥> scripts/dxl_ping.py <板用户>@<板IP>:/tmp/
ssh -i <私钥> <板用户>@<板IP> 'python3 /tmp/dxl_ping.py scan  --port /dev/ttyS2 --baud 1000000,57600'
ssh -i <私钥> <板用户>@<板IP> 'python3 /tmp/dxl_ping.py sync-read --port /dev/ttyS2 --ids 200,20,21,22,23,24 --addr 124 --length 12'
ssh -i <私钥> <板用户>@<板IP> 'python3 /tmp/dxl_ping.py probe --port /dev/ttyS2 --expect 10,11,12,13,14'
```

板 IP / 用户 → `wiki/concepts/zero3w-bench-plan.md`；**凭据只走本机 `~/.ssh`，不进仓 · 不回显**（红线 1）。

验收 = **同一条总线同时**认到 **ID 200（model 10200）＋ 腿 ID（model 1200）**，且
`sync-read` 那笔（就是官方 `refs/microduck/duck-control/src/bus.rs` 的形状）拿**非零**块 ——
输出里 `(no reply)` / **全 0** / 在变，是**三种不同结论**，别混（口径见判据真源）。
逐块 / 逐轮结论**回写 wiki**，别只留在本会话。

### C. 环境坑（都踩过）

- **Windows 上 `pyserial` 是硬前提** —— 脚本的 stdlib `termios` 回退**只在 Linux 上有**，而本仓刻意不加硬依赖（板子常无 `pip`）→ 开发机用 **`uv run --with pyserial`** 临时环境，**别改脚本**。
- **板侧别装包** —— 板上 `python3` 无 `pyserial` / `pip` 是常态；脚本自己退回 `termios` 就跑得起来。
- **传脚本必须 LF** —— Windows 发过去的 `.py` / `.sh` 带 CRLF，远程 Linux 报语法错。用 `scp` 原样传，或在 PowerShell 里 `-replace "\r\n","\n"` 重写换行。
- **`import dxl_ping` 要显式给路径** —— 远程脚本报找不到模块时用 `sys.path.insert(0, '/tmp')`，或把脚本放到 `dxl_ping.py` 同目录。
- **开发机 `python3` 是商店占位符** —— 用 `python` / `py -3.12`（详见 `wiki/concepts/local-workspace-layout.md`）。

**只读性** —— `read` / `sync-read` 与 `scan` / `info` 一样**只发 PING · READ · `0x82`**，不写任何寄存器；
写入仍归 `robotd` / Wizard（要写先列范围 ＋ 等用户确认）。
这两个子命令是 **2026-09-21 为本节补的**：`sync-read` 会把「**答了但块全 0**」单独报出来
（从机活、传感器死），`self-test` 用注入故障钉住广播地址 / 静默 ID / 空块三个分支。

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

该沉：编译 / flash 参数 · 总线抓包结论 · **板级分诊判据** · 板子 `python3` 缺 `pip` / `pyserial` 这类环境坑 · ONNX 契约变更记录。

已沉（2026-09-21）：**U2D2 逐块分诊 IMU 板** ＋ **主控远程验 IMU / 腿** → 见「板级诊断」节；
判据真源 `wiki/concepts/imu-to-dxl-firmware-triage.md`。过程坑：Windows **必须** `pyserial` · 传脚本 CRLF · `import` 路径。
同批补了 `scripts/dxl_ping.py` 的 **`read` / `sync-read`** 子命令（只读 · `self-test` 用注入故障验证）。

## 红线（本角色专属）

- **烧录量产固件 · 覆盖板上系统 · 写舵机寄存器** → 先列范围 ＋ 预检，**等用户确认**（`scripts/dxl_ping.py` 刻意只读）。
- 产物落 `imu_to_dxl/` · `image/` · `scripts/` · `microduck_ros2/`。
