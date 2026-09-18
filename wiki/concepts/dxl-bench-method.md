---
title: DXL 台架方法与脚本（参数 · 探测顺序 · 一致性基线）
created: 2026-09-16
updated: 2026-09-16
type: concept
tags: [dynamixel, servo, power]
sources:
  - https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/
  - ../refs/microduck/duck-control/src/bus.rs
  - ../refs/microduck/scripts/setup-board.sh
  - concepts/hat-dxl-bus-debug.md
confidence: high
related:
  - hat-dxl-bus-debug
  - xl330-cn-bench-kit
  - dynamixel-xl330
  - bench-power-supply
  - body-imu-hat-dxl-power-eval
---

# DXL 台架方法与脚本（参数 · 探测顺序 · 一致性基线）

> Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) 的**方法真源**：参数、探测顺序、脚本、一致性基线与 M1–M6 裁决。
> 步骤真源仍是 [[hat-dxl-bus-debug]]——本页只收「怎么判、用什么跑」。
> 手册真源：[XL330-M288 eManual](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)（2026-09-16 取）。

## 1. 台供参数（M1 / M2）

| 项 | 设定 | 依据 |
|----|------|------|
| 电压 | **6.0 V**（= 整机运行点，**辨识必须用此值**）；**6.0–6.5 V** 为调试可用带 | 手册 `Input Voltage` **3.7–6.0 V（推荐 5.0 V）**；`Max Voltage Limit(32)` 默认 **70 = 7.0 V**；实测 7.2 V 红灯持续闪。**整机定案（2026-09-18）：电池经降压模块稳定在 6.0 V 长期运行**，6.5 V 只是台架曾用值 |
| 电流限 | **纯 HAT 1 A**；**叠 Zero 2–3 A**；**上电前**按构型设好 | Zero 启动峰值 >1 A；台供 CC 触限是**拉低母线**、非干净断开 |
| 进电 | J13/J14 **针1=GND · 针2=+BATT** | 针2 就是 `+BATT`，**舵机不经 buck** → 台供电压 = 舵机电压 |
| 适用域 | HAT + Zero + **单**舵机、不开音频/ToF | 整机行走台供按 **5–10 A** 备（[[bench-power-supply]]） |

### 1.1 机制订正：`shutdown` 位（hardware 2026-09-16，据手册）

手册 `Shutdown(63)`：**bit0 = Input Voltage Error** · bit2 Overheating · bit4 Electrical Shock · bit5 Overload。

| 值 | 含义 |
|----|------|
| **53** | **出厂默认** = bit0+2+4+5，**含** Input Voltage |
| **52** | 官方 `robotd` 每轮启动写 = bit2+4+5，**清掉 bit0** → 官方配置**不**锁存 input-voltage |

- 旧说法「`shutdown=52` 锁存 input-voltage 并保持 torque off」方向**反了**（见 `robotd-design` §2.1 散文，与手册位表冲突，**以手册为准**）。
- 触发 `Shutdown` → 清 `Torque Enable(64)`、**红灯持续闪**，须**重启 / REBOOT 指令**才恢复。
- **过压是「转动」失效、不是「通信」失效**：shutdown 的舵机**仍应答 Ping/Read**。
  → **错电压本身不会造出「零回包」**；它造出「不动 / 报警 / 需重启」，**易被误读成不应答**。别据此漏掉真因。
- 详见 [[dynamixel-xl330]]（手册表）· [[body-imu-hat-dxl-power-eval]] §3.1。

## 2. 探测与出厂回退（M4）

新 XL330 **出厂 = ID 1 @ 57 600 baud**（手册 `ID(7)` 默认 1 · `Baud Rate(8)` 值 1(Default) = 57 600）。
官方 `open_bus`（`duck-control/src/bus.rs` `adopt` + `robotd-design` §2.1）：

1. 按 **1 Mbps** ping 预期 ID；
2. 若**恰好一个**不应答 → 探出厂舵机：先 ID 1 @ **1 Mbps**，再**重开端口 @ 57 600** 找 ID 1；
3. 写缺失 ID → 写总线波特率 → 回 **1 Mbps** → 查寄存器
   （`return_delay_time=0` · `baud_rate=3` · `pwm_slope=255` · `shutdown=52`）→ **重启舵机**
   （重启才清掉烧写留下的锁存 hardware-error，否则 torque 保持关）。

台架只有一只舵机 → 第 2 步在台架上是**手动**的；`probe` 会自动跑两段。
**只按 1 Mbps 测 = 假「零回包」。**

## 3. 一致性基线：官方 `setup-board.sh` `report()`（M6）

`MOTOR_PORT=/dev/ttyS2` · `REQUIRED_OVERLAY=uart2-m0`（流程原只写「UART2 overlay」，现点名）。

| `report()` 行 | 判定 |
|---------------|------|
| `motor bus` | ttyS2 在/不在；改了 overlay 会写「enabled, pending reboot」 |
| `motor bus owner` | **`fuser` 占用者 PID** vs `free` |
| `kernel console` | 区分**本次运行**（`/proc/cmdline`）与**下次启动**（`armbianEnv.txt`）；`console=display` 但本次仍打印 = **CONFLICT**（`extraargs=` / U-Boot 内建 bootargs 在赢） |
| `failed units` / `clock` | 启动阻碍 / 证书时间 |

`free_motor_port()` = mask `serial-getty@ttyS2`（**masked**，非 disable）+ `console=both/serial → display`。

**坑：`console=display` 重启才生效** —— 改的那一次运行里 console 仍打印，`report()` 会写「…, until the reboot」；
**重启后再跑一次**再判生效，别在未重启时判「改了没用」。

**取舍**：整脚本还会装音频/摄像头/ORT/vendor kernel —— 与本单 UART 排障无关且很重。
**要一致性**就跑全脚本并以 `report()` 为准；**只要 UART** 则取其 `free_motor_port`/`report` 语义即可。

## 4. M1–M6 裁决（2026-09-16 · hardware）

| 项 | 裁决 | 落点 |
|----|------|------|
| **M1** 母线 6.0–6.5 V | **确认**（机制订正见 §1.1） | [[hat-dxl-bus-debug]] §0 |
| **M2** 限流分段 | **确认** + 补「上电前按构型设定」 | §1 |
| **M3** #1 基线（ID/波特率/固件/电压） | 初判**证据不足**（#1 从未落真源）→ **复测已现场采集**，缺口关闭 | [[xl330-cn-bench-kit]] §测试结论 |
| **M4** 出厂 57 600 回退 | **确认** —— 且复测中它是**唯一**命中路径 | §2 |
| **M5** 版本化扫 / Ping 脚本 | **确认** → `scripts/dxl_ping.py` | `scripts/README.md` |
| **M6** 官方 `report()` 作一致性基线 | **确认** | §3 |

## 5. 脚本

`scripts/dxl_ping.py` —— **只读** Protocol 2.0 扫 / Ping / 基线读取；协议自实现，
**Linux 上零依赖**（有 `pyserial` 用之，无则退 stdlib `termios`——板子常无 `pip`）；带无硬件 `self-test`。

```bash
python3 scripts/dxl_ping.py self-test
python3 scripts/dxl_ping.py scan  --port COM7 --baud 1000000,57600
python3 scripts/dxl_ping.py info  --port COM7 --id <ID>
python3 scripts/dxl_ping.py probe --port COM7 --expect <ID列表>
```

**写 ID / 写波特率 / 寄存器修正不在脚本内**——归 `robotd` / Wizard。

### 5.1 两个已验证的坑（2026-09-16 台架）

1. **CRC 必须覆盖 4 字节 header**（`FF FF FD 00` 起）。漏掉 → 报文被舵机丢弃 → **两档波特率全「无回包」**，
   而 `self-test` 因为假舵机照抄同一错误会**全绿**。现由公开向量 `ff ff fd 00 01 03 00 01 19 4e` 钉死。
2. **本套件回包多一个固定字节 `0x55`**（`LEN = DATA + 4`，规格 `+3`），且在线上、被舵机 CRC 覆盖。
   按规格解析 → `error=0x55` 且**所有寄存器整体错位一字节**（`model=45056`、`1792.0 V` 这类「合理但错误」的值）。
   脚本用「PING 回 3 字节 / READ 回请求长度」自动判别两种帧；`self-test` 用实测帧回放回归。
   **该字节来源未定论**，需 U2D2 + Wizard 交叉验证。

## 6. 验收清单（Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) → 续 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)）

> **#4 已于 2026-09-16 关单**（原症状「未打通」不成立，HAT TTL 本来就通）。下列未勾项**全部移入 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)**。

**2026-09-16 复测（见 [[hat-dxl-bus-debug]] §8）——已勾**

- [x] 基线已记录：`dxl_ping.py info` 原始输出 → [[xl330-cn-bench-kit]]
- [x] **57 600 回退已试**，且是唯一命中（1 Mbps 全静默）
- [x] `/dev/ttyS2` 在 · getty masked · `fuser` 干净 · `console=display` 本次已生效
- [x] 软件 Ping/读寄存器成功（HAT 路径）

**仍未做**

- [ ] 示波器：空闲 DATA ≈3.3 V；Ping 主机包 + 回包波形
- [ ] 回包多出的固定字节 `0x55` 来源定论（U2D2 + Wizard 交叉验证）
- [ ] 按构型**实测**台供限流值（纯 HAT 1 A / 叠 Zero 2–3 A 仍为定案值，未实测复核）

**复查补充（主控↔HAT DATA 未打通）**

- [ ] **DXL 口是否真的上电** —— 针2 有压 ≠ 舵机口有压；先量舵机座子电压再谈通信
- [ ] **单变量原则** —— 换线/换舵机/换供电策略一次只动一个，评论里写明本次变量
- [ ] **分支定位（必须给结论）** —— ①供电未使能 ②串口被占用 ③物理层/方向脚 ④收发器或焊点 ⑤软件配置；证据不足也要写明
- [ ] **证据随单** —— pin2 电压 · pin3 空闲电平 · ping 主机包与回包波形 · 软件 ping/read ID 输出

## 7. 复测结果与要点（2026-09-16 · 已验证）

**HAT TTL 已打通。** `/dev/ttyS2` 在 · `hdy` 在 `dialout` 组 · getty **masked**/inactive ·
`fuser` rc=1（无占用）· `armbianEnv.txt` `console=display` 且 `/proc/cmdline` = `console=tty1`（**本次已生效**）·
`overlays=uart2-m0` + `overlay_prefix=rk3568`。
**1 Mbps 全静默 → 57 600 上 ID 1 应答**（model 1200）。舵机仍出厂状态 → [[xl330-cn-bench-kit]]。

复测要点：

1. **先确认波特率**：出厂舵机只答 **57 600**；1 Mbps 静默是**预期**，不是坏。
2. **先跑 `self-test`**：它现在用公开向量钉死 CRC 作用域。自检绿 ≠ 协议合规——要看到 `ff ff fd 00 01 03 00 01 19 4e`。
3. **读值要过常识**：`max_voltage_limit` 应 ≈70（7.0 V）、`present_input_voltage` 应 ≈ 台供电压。
   若出现 `1792.0 V` 这类值，是**帧错位**（本套件多一固定字节 `0x55`），不是舵机坏了。
4. **没装 `pyserial` 也能跑**：脚本在 Linux 上退回 stdlib `termios`。

**仍未做**：示波器波形 · 写 ID/波特率（归 `robotd`/Wizard）· `0x55` 来源定论（U2D2 + Wizard 交叉验证）。

相关：[[hat-dxl-bus-debug]] · [[xl330-cn-bench-kit]] · [[dynamixel-xl330]] · [[bench-power-supply]] · [[body-imu-hat-dxl-power-eval]]
