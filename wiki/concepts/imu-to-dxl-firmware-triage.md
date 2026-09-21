---
title: imu_to_dxl 板级诊断与验收
created: 2026-09-21
updated: 2026-09-21
type: concept
tags: [imu, firmware, board]
sources:
  - ../imu_to_dxl/firmware/src/lsm6dsv16x.c
  - ../imu_to_dxl/firmware/src/dxl_slave.c
  - ../refs/microduck/duck-control/src/bus.rs
  - ../refs/microduck/duck-control/src/imu.rs
confidence: high
related:
  - board-imu-to-dxl
  - imu-to-dxl-firmware-build
  - imu-to-dxl-v2
  - hat-dxl-bus-debug
  - dxl-bench-method
  - board-interconnect
  - tasks
---

# imu_to_dxl 板级诊断与验收

> 2026-09-21 实测结论：**「板子答 Ping」≠「IMU 能出数」** —— 两件事必须分开判。
> 流程**只读**（PING / READ / SYNC_READ），U2D2（COM7）与 HAT（`/dev/ttyS2`）都能跑。
> 编译 → [[imu-to-dxl-firmware-build]]；总线契约 → [[imu-to-dxl-v2]]。

## 0. 一句话

`imu_to_dxl` 的 **DXL 从机**与 **IMU 芯片**互相独立：MCU 起来了就会答 Ping；
**LSM6 死了只会让 12 B 数据块变全 0**，Ping 照答。**只做 Ping 会漏判。**

## 1. 两个观测面

| 读什么 | 地址 · 长度 | 说明 |
|--------|-------------|------|
| **数据块** | **124** · 12 B | gyro `i16`×3 ＋ quat `half` x/y/z（官方控制环读这个） |
| **诊断块** | **136** · 8 B | `u16` sample counter · `u8` status · accel raw |

`@124` 在 SFLP 未就绪时**输出全 0**（固件刻意：`!sflp_live` 时把 quat 清零）。

## 2. `@136` status —— 判板的第一道闸

`md_lsm6_poll()` 每轮置位（`lsm6dsv16x.c`）：

| status | 含义 | 卡在哪 |
|--------|------|--------|
| `0x00` | IMU 全无 | **`md_lsm6_init()` 卡在 `WHO_AM_I(0x0F)`**，连 `present` 都没置 → SPI / 供电 / 芯片 |
| `0x01` | present，SFLP 未出 | `present` 已置，SFLP 还没给四元数 |
| `0x03` | **IMU ok ＋ SFLP live** | ✅ 正常 |
| `0x05` | SFLP 配置失败 | `emb_enter` / `wr_verify`（EMB_FUNC 那几个写）失败 |

**counter 必须递增** —— 它是主机 stale 检测的锚（`bus.rs` `StaleImuTracker`）；全 0 或不动 = 死的。

## 3. 坑：官方事务对「IMU 死的板」会**静默成功**

`duck-control` 每 tick 一笔 `sync_read(ids, 124, 12)`（`bus.rs`）。IMU 死的板**照样答**，于是：

- 返回 **12 个零字节**，`sync_read` **不报错**；
- `SflpDecoder::ready()` 永远为假、stale 计数一路飙（`imu.rs`）；
- 反过来，IMU **完全不答**（`sync_read` 少一个 id）会让**整笔失败** → daemon 起不来。

所以「daemon 没报错」**不能**证明 IMU 在工作；读 `@136`、或 `sync-read` 打出的「**答了但块全 0**」标注，才能把它们分开。

## 4. 只读判定流程（一块一块来）

```bash
python3 scripts/dxl_ping.py scan  --port COM7 --baud 1000000,57600   # 先看有没有 model 10200
python3 scripts/dxl_ping.py read  --port COM7 --id 200 --addr 124 --length 12   # 数据块
python3 scripts/dxl_ping.py read  --port COM7 --id 200 --addr 136 --length 8    # 诊断块
```

**跑两趟 `@136`，比 counter 是否递增** —— 单次读数分不出「活的静止」与「冻死的」。

**`info` 的 fw 会错位**：它按 XL330 表读**地址 6**，而本板 fw 在**地址 2**（`control_table.c`）→ 以 **Ping 回包 bytes 0/1/2** 为准。
这也是 `read` / `sync-read` 存在的理由（`scripts/README.md`）：`info` 是 XL330 形状的，看不了自己不认识的表。

## 5. 2026-09-21 逐块结果（U2D2 COM7 · 5 V · 只读）

| 板 | `ping 200` | `@136` | 判 |
|----|-----------|--------|-----|
| **2 号** | ✅ model 10200 | `0x00` · counter=0 · `@124` 全 0 | DXL 在跑 · **IMU 芯片/SPI 坏** |
| **3 号** | ✅ model 10200 | **`0x03`** · counter 8075→8117 · 数据活 | ✅ **USABLE** |
| **1 号** | ❌ 无应答 | — | **SWD 也「找不到设备」** → MCU 侧 |
| 4 / 5 号 | — | — | 未焊完 |

「答 Ping 与否」**只有逐块插**才分得出 —— 同一批板里两种坏法都有。

## 6. HAT 路径复核（同日）

**3 号板**经 **J13**、**后面串 #20**：

- `ping 200` / `ping 20` 都答；全扫得 `20–24` ＋ `200(10200)`；
- **`sync-read --ids 200,20,21,22,23,24 --addr 124 --length 12` 拿到非零块**；`@136 status=0x03`、counter **~100 Hz** 递增；
- quat 稳定、gyro 逐帧变 → 板静止、采样真活；
- → **HAT 链路 ＋ IMU 板 inline 中继都成立**，与 [[hat-dxl-bus-debug]] 的「HAT 已打通」一致。
  推论：**「HAT 上 IMU 静默」不是 HAT 的问题**，是那块板自己的问题。

## 7. 与官方读取方式的一致性（逐条对过）

| 项 | 官方（`bus.rs` / `model.rs`） | 固件（`md_config.h` / `dxl_slave.c`） |
|----|------------------------------|--------------------------------------|
| ID · 波特率 | 200 · 1 Mbps | 200 · 1 Mbps（USART2 `BRR=16`） |
| 读法 | 合并 `sync_read`，IMU 在 `ids[0]` | `INST_SYNC_READ(0x82)`，addr/len 从参数取 |
| 块 | addr **124** · **12 B** | 同 |

**写白名单只放 `addr 9` 与 `20–29`** → **ID(7) / 波特率(8) 不可写**，板子必然固定 `200 @ 1 Mbps`
→ 「它在别的地址/波特率上」在算术上不成立。

**结论：固件侧无接口偏差**；「IMU 读不到」的原因在**板**（芯片 / SPI / 焊接），不在协议。

## 8. 归属

- 2 号板「DXL 活 / IMU 死」、1 号板「SWD 找不到设备」= **硬件**（LSM6 供电 · SPI · MCU）→ hardware。
- 装机用 **3 号板** —— [[tasks]] `T-02` 的 IMU 侧判据达成。

相关：[[board-imu-to-dxl]] · [[imu-to-dxl-firmware-build]] · [[hat-dxl-bus-debug]] · [[dxl-bench-method]] · [[board-interconnect]]
