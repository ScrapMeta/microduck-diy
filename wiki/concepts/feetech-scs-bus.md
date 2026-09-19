---
title: 飞特 SCS 总线协议
created: 2026-09-19
updated: 2026-09-19
type: concept
tags: [servo, feetech, runtime, sim2real]
sources:
  - refs/microduck-replica/docs/飞特资料/SCS通信协议-v1.0-2026-06-09.md
  - refs/microduck-replica/docs/飞特资料/磁编码STS内存表手册-v1.1-2026-08-27.md
  - refs/microduck-replica/software/飞特适配架构.md
confidence: high
related:
  - feetech-hd-1910
  - dynamixel-xl330
  - microduck-replica
  - bam-identification-bench
---

# 飞特 SCS 总线协议

飞特 STS/SMS/HLS 系列的自定义总线协议。**核心结论：SCS 是 Dynamixel Protocol 1.0 的血统，
不是 2.0——但寄存器表完全不同。**

依据：飞特官方《舵机 SCS 通信协议》v1.0（2026-06-09）与《磁编码 STS 内存表手册》v1.1
（2026-08-27），副本在 `refs/microduck-replica/docs/飞特资料/`。

## 1. 帧格式：与 DXL 1.0 逐字相同

```
飞特 SCS    FF FF  ID  LEN  INSTR  …PARAMS  CHK      CHK = ~(ID+LEN+INSTR+ΣPARAMS) & 0xFF
DXL 1.0     FF FF  ID  LEN  INSTR  …PARAMS  CHK      同上（逐字相同）
DXL 2.0     FF FF FD 00  ID LEN INSTR …PARAMS  CRC16_L CRC16_H
```

- `LEN = 参数长度 + 2`
- 8N1，1 起始 / 8 数据 / 1 停止，无校验位
- **磁编码系列（STS/SMS/HTS）两字节小端**；电位器型大端。STS 小端 = 与 DXL 一致
- ID 0–253，**广播 254**（DXL 2.0 保留 253，飞特把它当合法 ID）

**改写协议 = 改帧头 + 改校验算法**，不是从零写。这正是适配成本低的原因。

## 2. 指令表

| 值 | 飞特 | DXL |
|---|---|---|
| 0x01 / 0x02 / 0x03 | PING / READ / WRITE | 同 ✅ |
| 0x04 / 0x05 | REG_WRITE / ACTION | 同 ✅ |
| 0x82 / 0x83 | SYNC_READ / SYNC_WRITE | 同（2.0 才有）|
| **0x08** | **重启**（约 800 ms，无应答，先关扭矩）| **同码同义** ✅ |
| 0x06 | 参数恢复（恢复 0x09 备份，ID 除外，须先解锁）| FACTORY_RESET |
| 0x09 / 0x0A | 参数备份 / 状态重置（清圈数）| — |
| 0x0B | 位置校准（无参=校为中位；STS ≥ 3.10 支持带参）| — |

> ⚠️ **`0x06` 不是「恢复出厂」**：它是「恢复 0x09 备份过的参数」。2019 版手册里
> 才是恢复出厂——**依据旧手册或 SDK 头文件会得出错误结论**（replica 与两轮评审
> 都曾因此断言「飞特没有 REBOOT」）。

## 3. 寄存器表：与 XL330 无一处运动核心同址

| 功能 | XL330 | HD-1910 / STS |
|---|---|---|
| ID | 7 | **5** |
| 波特率 | 8（`3` = 1 M）| **6**（`0` = 1 M）|
| 回包延时 | 9（出厂 250，**必须清 0**）| **7 是预留** → 不用管 |
| 运行模式 | 11 | **33** |
| 目标位置 | **116**（i32）| **42**（i16）|
| 当前位置 | **132**（i32）| **56**（i16）|
| 速度 | 128（i32，0.229 rpm/c）| **58**（u16）|
| 电流 | 126（i16，mA）| **69**（u16，**6.5 mA/单位**）|
| 电压 / 温度 | 144 / 146 | **62 / 63** |
| **P / I / D 增益** | 84 / 82 / 80，u16，**RAM**，0–16383 | **21 / 23 / 22**，u8，**EEPROM**，0–254 |
| 扭矩开关 | 64 | **40**（0 关 / 1 开 / **2 阻尼** / 128 中位校准）|
| 硬件错误 | 70（+ `shutdown` 52 掩码）| **65**（+ `卸载条件` 19，同位定义）|
| 锁 | 55 | **55** ✅ |

温度上限(13) 与锁(55) 两处同址——都继承 AX-12 血统，其余全改过。

**唯一免换算的量是位置**：两侧都是 4096 步/圈、2048 = 中位，
`rad = 2π·raw/4096 − π`。其余全部要换算。

## 4. 两个会伪装成「舵机没劲」的坑

### 符号位编码不同

飞特位置/速度/电流用 **BIT15 作方向位（符号-幅值）**，负载用 **BIT10**；DXL 用**二进制补码**。

```
飞特速度寄存器 0x8001  →  实为 −1
按 DXL 补码解码       →  −32767    ← 差 3 万倍，且不报错
```

位置寄存器在舵机模式只用 0–4095，两种编码恰好一致——**所以「位置读对了」不能证明解码对了**。
属于本项目反复遇到的那一类「合理但错误」（[[dynamixel-xl330]] 的 `max_voltage_limit=1792.0 V`、
`model=45056` 同理）。

### 增益在 EEPROM —— 但「锁着写」正好当 RAM 用

XL330 的 P/I/D 在 RAM，运行中随便写；飞特的 21/22/23 在 **EEPROM 区（5–39）**，
照 XL330 的写法（走↔站↔倒地每次切状态都写一轮）会**磨穿 EEPROM**。

内存表 55 原文：*「写 1 打开写入锁，写入 EPROM 地址的值**掉电不保存**」*。

→ **锁着写**：不解锁直接写 P = **写入被接受、只是不落盘**，正好是 XL330 的 RAM 语义。
零磨损，且重启回到 EEPROM 值与 `reboot` 契约一致。

> 另一处差异：**D 不要清零**。XL330 版把 I/D 写 0 是因为出厂就是 0；飞特出厂 D = 32
> 是厂家整定的一部分——320:1 的高减速比去掉 D 可能振荡。

## 5. 工具链与库

| 来源 | 内容 | 语言 |
|---|---|---|
| 飞特官方 | `fddebug`（FD 上位机，Windows，MIT）· `FTServo_Linux` · `FTServo_Python` | C/C++ · Python · **全在 Gitee，无 Rust** |
| **rustypot** | `feetech/{sts3215, scs0009, scs0043}.rs` + `dynamixel_protocol/v1.rs` | **Rust** |
| 社区 | `DoraCN/feetech-servo-sdk`（MIT，tokio）| Rust |

官方 `duck-control` 已依赖 **`rustypot = "1.6.0"`**（Pollen 自家库），而它**已带飞特 STS 内存表**。
据 [[microduck-replica]]：`v1.rs` 实现了 `SyncRead = 0x82`/`SyncWrite = 0x83`——
**Dynamixel 1.0 本身没有 0x82，这是为飞特加的**。

> ⚠️ rustypot 未在本工作区安装或 vendored，**此条我方尚未独立复核**；
> 依据是 replica 的 `software/飞特适配架构.md`（作者读的是 rustypot 1.6.0 源码）。

[[microduck-replica]] 另外自己写了 `tools/servo-web/feetech.py`（约 100 行，不依赖官方 SDK，
直接按手册发包），可作 `scripts/dxl_ping.py` 的对称参照。

## 6. 实现：代价收敛在一个 trait 后面

官方运行时的接缝是 `duck-control/src/io.rs` 的 **`RobotIo`**（读 / 写 / 设增益 / 设扭矩 /
重启 / 慢传感器）。已有 `DynamixelIo`（真机）、`FakeIo`、`RemoteIo`（仿真）三个实现，
**飞特是第 4 个**——控制环、策略、安全、IPC、`robotctl` 一行不动。

四个真难点：

| # | 难点 | 处置 |
|---|---|---|
| 1 | 增益在 EEPROM | **锁着写**（§4）|
| 2 | **IMU 不在总线上**——官方 `imu_to_dxl` 板是 DXL 从机（ID 200），飞特总线接不上 | A：重写小板固件冒充飞特 ID 200；**B：BNO085 直飞 I2C（先做）** |
| 3 | 出厂模式是 **4**，不是 0 或 3 | 断言 `33 == 4`；通用手册只列 0–3 |
| 4 | **应答级别必须 = 1** | 手册：`0` = 除读/PING 外不回包 → rustypot 每笔写超时 30 ms，15 颗拖垮 init |

第 2 条是**换协议最容易被忽略的连带代价**：官方把 IMU 做成总线从机，
**协议一换，这个设计就断了**。

> ⚠️ 模式 4 在两个官方来源里含义不一致（HD-1910 规格书「恒流/PWM」vs 通用 STS 表
> 「PWM/步进」）→ **以实机读出的底账为准**。同一寄存器在不同固件上语义漂移，
> 是无声错误的高发区。

## 7. 对换执行器评估的意义

[[xl330-vs-kpower-rd05t]] 的头号阻塞是「寄存器表未知」。**飞特提供了对照组**：

| | 飞特 HD-1910 | RD05T |
|---|---|---|
| 协议 | **已知且不同**（内存表公开，逐地址可查）| **未知**（规格书只给物理层）|
| 工作量 | 明确：约 500 行后端 + 库现成 | 取决于未知数：真兼容 ≈ 0，不兼容 = 出局 |
| 风险类型 | **工程风险**（可测、可分阶消）| **信息风险**（只能等厂商或实测）|

**飞特证明「换协议」本身不是障碍**——所以 RD05T 的判定不该卡在「协议不同怎么办」，
而应聚焦「**它到底是不是真 DXL、P 增益能否写**」，即 [[bam-identification-bench]]
的电气闸门与 `scripts/servo_swap_compare.py` 的守卫已在检的那两件事。

相关：[[feetech-hd-1910]] · [[dynamixel-xl330]] · [[microduck-replica]] · [[bam-identification-bench]]
