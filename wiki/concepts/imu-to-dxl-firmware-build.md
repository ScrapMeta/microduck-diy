---
title: imu_to_dxl 固件编译（Agent 手册）
created: 2026-09-14
updated: 2026-09-15
type: concept
tags: [firmware, imu, diy]
sources:
  - concepts/board-imu-to-dxl.md
  - concepts/firmware-flash-matrix.md
  - https://github.com/ScrapMeta/microduck-diy/issues/10
confidence: high
related:
  - board-imu-to-dxl
  - firmware-flash-matrix
  - imu-to-dxl-ref-schematic
  - imu-to-dxl-v2
  - local-workspace-layout
  - diy-milestones
---

# imu_to_dxl 固件编译（Agent 手册）

> 给其他 agent：**只编译/单测**可按本页；烧录需 ST-Link + 板。  
> 仓路径：`imu_to_dxl/` · 硬件真源 **v0.3** · 板卡入口 [[board-imu-to-dxl]]。  
> 契约真源仍以仓内 `README.md` + `docs/` 为准；冲突以仓为准并回写本页。

## 0. 产出与验收

| 目标 | 命令 | 产物 / 判据 |
|------|------|-------------|
| 主机单测 | `make host-test` | 进程 exit 0（CRC / pack / 控制表） |
| 板端镜像 | `make g031` | `firmware/build/imu_to_dxl.elf` + `.bin` · `arm-none-eabi-size` 有输出 |
| 烧录（可选） | `./scripts/flash_openocd.sh` | OpenOCD `verify` 成功 |

**本页默认不要求烧板**；无硬件时做到 `make g031` 即完成编译任务。

## 1. 工程位置

```
imu_to_dxl/
  README.md
  docs/protocol.md · hardware.md
  firmware/          # Makefile 在此
  scripts/           # flash_openocd.sh · debug_openocd.sh
```

脚位宏：`firmware/include/md_config.h` · 板级：`firmware/platform/stm32g031/board_g031.c`（对齐 v0.3）。

## 2. 工具链（WSL / Linux 推荐）

Windows 宿主请在 **WSL** 里编（与仓库路径 `/mnt/d/projects/microduck/...` 一致即可）。

```bash
sudo apt-get update
sudo apt-get install -y build-essential gcc-arm-none-eabi binutils-arm-none-eabi
# 仅烧录/调试时再装：
# sudo apt-get install -y openocd gdb-multiarch
```

检查：

```bash
arm-none-eabi-gcc --version
gcc --version
```

不需要 STM32CubeIDE / CubeMX 也能出镜像（自带 startup + ld）。

## 3. 编译步骤（复制即用）

```bash
cd /mnt/d/projects/microduck/imu_to_dxl/firmware   # 按本机根路径改
make clean
make host-test
make g031
ls -l build/imu_to_dxl.elf build/imu_to_dxl.bin
arm-none-eabi-size build/imu_to_dxl.elf
```

交叉前缀默认 `arm-none-eabi-`；可覆盖：`make g031 CROSS=arm-none-eabi-`。

### 常见失败

| 现象 | 处理 |
|------|------|
| `arm-none-eabi-gcc: not found` | 安装 `gcc-arm-none-eabi` |
| `host-test` 链接 `-lm` 失败 | 装 `build-essential` |
| 路径在 PowerShell 下 `make` 怪异 | 改走 WSL bash |
| 旧名 `microduck_imu_to_dxl/` | 已迁到 `imu_to_dxl/`；勿编错仓 |

## 4. 烧录 / 调试（可选）

调试口 **J2 BM07**：2=SWCLK · 3=SWDIO · 4=GND · 7=NRST（详表见仓 `README` / [[imu-to-dxl-ref-schematic]]）。

```bash
cd imu_to_dxl
./scripts/flash_openocd.sh
# 或：./scripts/flash_openocd.sh firmware/build/imu_to_dxl.elf
```

OpenOCD：`interface/stlink.cfg` + `target/stm32g0x.cfg`。调试：`./scripts/debug_openocd.sh` 后 `gdb-multiarch build/imu_to_dxl.elf` → `target extended-remote localhost:3333`。

## 5. 总线契约（联调时对照）

| 项 | 值 |
|----|-----|
| Protocol | Dynamixel **2.0** |
| ID | **200** |
| Baud | **1 000 000** |
| sync_read | addr **124** · **12 B** |
| 布局 | gyro `i16` LE ×3 + quat xyz IEEE half LE |

主机解码：`refs/microduck/duck-control/src/imu.rs`。矩阵总览：[[firmware-flash-matrix]]。

## 6. Agent 回写清单

编译完成后在 Issue/聊天注明：

1. `make host-test` / `make g031` 是否通过  
2. `imu_to_dxl.elf` 路径与 `size` 一行  
3. 若烧录：OpenOCD 是否 verify；未烧则写「仅编译」

## 7. Issue #10 产物与 U2D2 台架（2026-09-15）

| 项 | 值 |
|----|-----|
| Commit | `a49a628`（`imu_to_dxl/firmware/`） |
| Issue | [#10](https://github.com/ScrapMeta/microduck-diy/issues/10) · `ready-for-pm` |
| 构建 | `make clean && make host-test && make g031` · exit 0 |
| `size` | text **4328** · data **0** · bss **1512** · dec **5840** |
| ELF SHA-256 | `3670fb4deb8618f43c5e42c8e99053dcab5ba3a7b21da50e72fb3f91c734129a` |
| BIN SHA-256 | `7b630d450c66bbcb7e4658617163b4c44532b5f7c5f52b30a7f539d5ec9b1277` |
| GPIOA | 保留 #6：`IOPORT_BASE=0x50000000` |

**U2D2 实板（COM7 · Protocol 2.0 · 1 Mbps · 单挂 ID 200 · `dynamixel_sdk`）：**

| 项 | 结果 |
|----|------|
| Ping | Model **10200** · 1000/1000 · 0 错 |
| Read(124,12) | 1000/1000 · 0 丢包/CRC/短包 · 载荷持续变化 |
| @136 诊断 | status **`0x03`**（IMU present + SFLP live）· sample counter 递增 |
| GroupSyncRead(124,12) | ~50 Hz × **10 min** · **30000** ok · **0** timeout · **0** ShortRead |

Stuffing / 越界读写：host-test 覆盖；实板未另做线上抓包。波形/示波器仍可归 [#7](https://github.com/ScrapMeta/microduck-diy/issues/7) 收口。

相关：[[board-imu-to-dxl]] · [[firmware-flash-matrix]] · [[local-workspace-layout]] · [[imu-to-dxl-v2]] · [[diy-milestones]]
