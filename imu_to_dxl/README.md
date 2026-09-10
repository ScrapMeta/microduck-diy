# imu_to_dxl

机身 **imu_to_dxl** 参考板固件 + 硬件工程（**非官方**）。在 Dynamixel TTL 总线上以 **ID 200** 应答，与 HAT / `duck-control` 的 `sync_read` 契约对齐。

> **路径：** `microduck-diy/imu_to_dxl/`  
> **硬件现行：v0.3** — 真源 `hardware/imu_to_dxl_ref_2026-08-30_18-59-47.eprj2` · 脚位见 [`docs/hardware.md`](docs/hardware.md)。

## 契约（与主机一致）

| 项 | 值 |
|----|-----|
| 协议 | Dynamixel **2.0** |
| ID | **200** |
| 波特率 | **1 000 000** |
| 控制环读地址 | **124** |
| 长度 | **12 B**（可选扩展诊断至 20 B） |
| 布局 | gyro `i16` LE ×3（±500 dps）+ quat x/y/z **IEEE half** LE；`w` 由主机重建 |

权威解码：工作区 `microduck/duck-control/src/imu.rs` · `bus.rs`。Wiki：`board-imu-to-dxl` / `imu-to-dxl-ref-schematic`。

## 硬件（**v0.3** 定稿）

- MCU: **STM32G031F8P6**
- IMU: **LSM6DSV16X**（SPI + 片上 **SFLP**）
- 半双工: USART2 + **SN74LVC1G125**（`OE#` 低=TX）
- 座：双 **B3B-EH**（J1/J3）· 调试 **BM07 7P**（J2）
- LDO: **AP2210K-3.3**；保护：PESD + 5.1 V + R6

| 功能 | 脚 |
|------|-----|
| DXL DIR / OE# | **PA1** |
| USART2 TX / RX | **PA2 / PA3** |
| SPI1 CS/SCK/MISO/MOSI | **PA4 / PA5 / PA6 / PA7** |
| IMU INT1（可选） | PA0 |
| SWD | PA13 / PA14 |
| USART1 TX / RX（J2 调试） | PA11 / PA12 |
| NRST | PF2 → J2-7 |

完整网表 / 连接器：[`docs/hardware.md`](docs/hardware.md)。v0.2 板不再作装机真源。

## 目录

```
imu_to_dxl/   （或暂用旧名 microduck_imu_to_dxl/）
  README.md
  docs/protocol.md · hardware.md
  hardware/           # eprj2 真源 + README
  firmware/
  scripts/
```

## 主机侧单测

```bash
cd firmware
make host-test
```

## 板端构建

```bash
cd firmware
make g031
```

产出：`build/imu_to_dxl.elf` / `.bin`。

### 调试口 J2（BM07 · 可看的接口信息）

| Pin | 网名 | MCU | 用途 |
|-----|------|-----|------|
| 1 | +3V3 | — | 板子供电 / 与调试器共电源（按线束） |
| 2 | SWCLK | PA14 | **SWD 时钟** → ST-Link |
| 3 | SWDIO | PA13 | **SWD 数据** → ST-Link |
| 4 | GND | — | 地 |
| 5 | UART1_TX | PA11 | 调试串口 MCU→PC（固件**尚未**打日志） |
| 6 | UART1_RX | PA12 | 调试串口 PC→MCU |
| 7 | NRST | PF2 | 复位（推荐接 ST-Link NRST） |

完整网表：[`docs/hardware.md`](docs/hardware.md)。脚位宏：`firmware/include/md_config.h`。

**现在能「看到」什么**

| 通道 | 能看到 | 条件 |
|------|--------|------|
| SWD + GDB/CubeIDE | 断点、变量、内存、外设寄存器 | ST-Link + OpenOCD（或 STM 工具） |
| J2 UART1 | 文本日志 | 需以后在固件开 USART1 + printf；**当前无输出** |
| DXL 总线 | ID 200 @124 的 12 B | 主机 `sync_read` / 逻辑分析仪 |

### 烧录

```bash
# 在 imu_to_dxl/ 下（WSL 需已装 openocd）
./scripts/flash_openocd.sh
# 或：./scripts/flash_openocd.sh firmware/build/imu_to_dxl.elf
```

### SWD 调试（OpenOCD + GDB）

```bash
# 终端 1：挂住芯片
./scripts/debug_openocd.sh

# 终端 2
cd firmware
gdb-multiarch build/imu_to_dxl.elf
# (gdb) target extended-remote localhost:3333
# (gdb) monitor reset halt
# (gdb) load          # 可选：顺带重烧
# (gdb) break main
# (gdb) continue
```

也可用 **STM32CubeIDE / CubeProgrammer** 烧同一 `imu_to_dxl.elf`，调试口仍是上表 J2。

## 软件架构

```
┌─────────────┐   SPI    ┌──────────────┐
│ LSM6DSV16X  │◄────────►│ lsm6dsv16x.c │──SFLP FIFO──┐
└─────────────┘          └──────────────┘             │
                                                      ▼
                                               imu_pack.c ──► control_table[124..]
                                                      ▲
┌─────────────┐  USART2  ┌──────────────┐             │
│ HAT / robotd│◄────────►│  dxl_slave   │◄────────────┘
│ sync_read   │  半双工   │  Protocol2  │
└─────────────┘          └──────────────┘
```

## 状态

| 模块 | 状态 |
|------|------|
| 硬件 v0.3 工程 / 文档 | ✅ 真源 eprj2 + hardware.md |
| DXL 2.0 从机 / 控制表 @124 | ✅ |
| G031 板级驱动 | ✅ 对齐 v0.3 脚；USART1 串口日志尚未启用 |
| 官方坐标/20 B 诊断 | ⚠ 自约定 |

## 许可

固件与文档：**MIT**。主机契约来自开源 `duck-control`；ST 行为参考公开 datasheet（勿与官方闭源固件混称）。
