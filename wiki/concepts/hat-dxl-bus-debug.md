---
title: HAT TTL 舵机测不通排查
created: 2026-09-14
updated: 2026-09-21
type: concept
tags: [hat, dynamixel, bench]
sources:
  - concepts/hat-solder-kit.md
  - concepts/xl330-cn-bench-kit.md
  - ../refs/microduck/scripts/setup-board.sh
  - ../refs/microduck/duck-control/src/bus.rs
  - https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/
confidence: high
related:
  - hat-solder-kit
  - board-hat
  - board-interconnect
  - xl330-cn-bench-kit
  - dynamixel-xl330
  - zero3w-bench-plan
  - dxl-bench-method
---

# HAT TTL 舵机测不通排查

> 针对：**U2D2 台架曾通过**，叠 [[elec-rpi-robot-hat]] + Zero 后扫不到 / timeout。  
> Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)（**closed 2026-09-16**）——原症状不成立：HAT TTL 本来就通，
> 真因是**测试前提错**（该舵机仍出厂 ID 1 @ 57 600）+ **脚本 CRC 作用域 bug**。剩余项见 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)。  
> 工装：**双通道示波器** + **30 V / 10 A 可调电源**（电流可限）。  
> 焊接/485：[[hat-solder-kit]]。接线：[[board-interconnect]]。

官方 `setup-board.sh` 写过同一症状：`read return_delay_time on 20: Operation timed out`，舵机在 U2D2 上正常——**getty 把回包读走了**。

## 0. 台供与只接 1 只舵机

> 参数依据 · 机制订正（`shutdown` 位）· 限流分段 · 探测顺序 · 一致性基线 → **[[dxl-bench-method]]**。本页只留台架要照做的值。

| 项 | 设定 |
|----|------|
| 电压 | **6.0 V 优先**；**6.0–6.5 V** 为实测可用带（手册上限 6.0 V）；**勿** 7.4 V 直供舵机 |
| 电流限 | **纯 HAT 阶段 1 A**；**叠 Zero 后 2–3 A**；**按当前构型在上电前设好** |
| 进电 | J13 或 J14：**针1=GND · 针2=+BATT**（针脚 **1=GND · 2=VBATT · 3=DATA**；与部分飞特线序相反）；针3 先空 |
| 禁止 | >6.5 V 直供舵机、30 V、Type-C 与 `+BATT` 同时灌、一次挂多只 |

---

## 1. 先证明舵机还活着（绕开 HAT）

用已通过的 [[xl330-cn-bench-kit]]：**PC → U2D2/PHB → 同一只 XL330**。

| 结果 | 含义 |
|------|------|
| U2D2 能扫到 | 舵机/线/ID/波特率 OK → 问题在 **HAT / Zero / 软件** |
| U2D2 也扫不到 | 先修舵机电源、线序；再按 §1.1 走 **1 Mbps → 57 600** 探测顺序（别只按 1 Mbps 就判死） |

记下：**ID、波特率、固件、当时电压**，后面 HAT 必须用同一套。用脚本采原始输出（勿手抄）：

```bash
python3 scripts/dxl_ping.py info --port COM7 --id <当前ID>   # 基线：ID/波特率/固件/电压
```

### 1.1 出厂默认回退（1 Mbps 扫不到 ≠ 硬件坏）· 订正 M4

新 XL330 **出厂 = ID 1 @ 57 600 baud**——两者**本总线都不用**。**只按 1 Mbps 测会得到假「零回包」**：
先按 1 Mbps ping 预期 ID；若恰一个缺失 → 探 ID 1（先 1 Mbps、再**重开 57 600**）→ 写 ID/波特率 → 回 1 Mbps →
查寄存器 → **重启舵机**（重启才清烧写留下的锁存 hardware-error）。顺序与寄存器 → **[[dxl-bench-method]] §2**。

---

## 2. 电源（HAT 路径，先不发总线）

台供 **6.0–6.5 V** → J13 针2/针1。叠 Zero，系统已能亮屏。

| # | 测 | 期望 | 失败 |
|---|-----|------|------|
| 2.1 | 台供电流（**纯 HAT**，不叠 Zero、不接舵机） | 数十 mA 级 | 顶死 1 A → 短路，先别接舵机 |
| 2.1b | 叠 Zero 后（不接舵机） | 亮屏 idle 约 **0.2–0.8 A**；**启动峰值可超 1 A** | 限流触顶 → 母线塌陷 → 表现成「不启动 / 无 `ttyS2`」，**勿误判成焊接或 overlay 故障** |
| 2.2 | J13 **针2↔针1** | ≈ 台供电压 | 无压：座虚焊 / 没接到 `+BATT` |
| 2.3 | J4 **5V / 3V3** | ≈5.0 / ≈3.3 | 见 [[hat-solder-kit]] §4 |
| 2.4 | 再插 **1 只** 舵机，针2 仍≈台供电压 | 电流多 **0.1–0.3 A** | 电流暴涨 → 线序反 / 舵机损坏 |

---

## 3. Zero 软件（最常见：口被占用）

SSH 进板（或本机终端）：

```bash
ls -l /dev/ttyS2
sudo fuser -v /dev/ttyS2
systemctl is-enabled serial-getty@ttyS2.service
grep -E '^(console=|overlays=|overlay_prefix=)' /boot/armbianEnv.txt
```

| 检查 | 要通过 |
|------|--------|
| `/dev/ttyS2` 存在 | 无则 overlay：`overlay_prefix=rk3568` + **`overlays=uart2-m0`**（`setup-board.sh` 的 `REQUIRED_OVERLAY`；`overlay_prefix=rk35xx` 在本板是**错的**，会静默丢口） |
| `fuser` | **不能**是 `agetty` / `getty` |
| getty | 必须 **masked**（只 disable 会被 `getty.target` 拉回来） |
| `console=` | 必须 **`display`**，不能是 `both` / `serial`（内核 printk 会打坏回包） |

修完**重启**再扫。未跑 `provision` / `setup-board.sh` 时，上面几乎必挂。**`console=display` 重启才生效**。

扫总线用可版本化脚本（勿再靠「板上已装工具」）：

```bash
python3 scripts/dxl_ping.py scan  --port /dev/ttyS2 --baud 1000000,57600   # 先 1 Mbps，再 57 600 回退
python3 scripts/dxl_ping.py info  --port /dev/ttyS2 --id <ID>              # 基线：ID/波特率/固件/电压
python3 scripts/dxl_ping.py probe --port /dev/ttyS2 --expect <ID列表>      # 复刻官方探测顺序
```

- 官方栈：`robotd` / 仓库自带 ping
- Dynamixel Wizard / SDK：端口 **`/dev/ttyS2`**，**1 000 000**，Protocol **2.0**

一致性基线用官方 `setup-board.sh` 的 `report()`（`fuser` 占用者 PID · console 冲突 · `uart2-m0`）→ **[[dxl-bench-method]] §3**。

---

## 4. 示波器（2 路）

共地：探头地夹 **HAT GND**（J13 针1）。带宽 ≥20 MHz。时基先 **2 µs/div**（1 Mbps 一位 = 1 µs）。

### 4.1 探点

| 通道 | 夹 | 看什么 |
|------|-----|--------|
| **CH1** | J13 **针3 DATA** | 总线波形 |
| **CH2** | **Dynamixel_dir**（U6/U7 附近丝印 / `Dynamixel_dir` 网）或 J4 上 UART2 **TX** | 方向 / 主机发送 |

触发：**CH1 下降沿**，单次。然后在 Zero 上对已知 ID **Ping / 读一次**。

### 4.2 空闲（不发命令）

| 现象 | 判断 |
|------|------|
| CH1 ≈ **3.3 V** 高电平 | 正常（LVC 半双工，空闲释放） |
| CH1 ≈ 0 V | 总线被拉死（桥锡、U6 一直使能、短路） |
| CH1 悬浮乱跳 | 缺上拉 / PHY 没焊好（查 U5/U6/U7、R29） |

### 4.3 只发、不接舵机

Ping 一次应看到 **CH1 一串 3.3 V UART 包**（约 1 Mbps）。

| 现象 | 判断 |
|------|------|
| 无任何边沿 | UART 没出 HAT：ttyS2 / overlay / J4 虚焊 / 探错脚 |
| 有包，位宽不是 ~1 µs | 波特率不是 1 Mbps |
| 幅度 << 2 V | 驱动弱或探头衰减；查 3V3、U6 |

CH2 在发包期间应变成 **发送态**，包结束后应回到 **接收态**（官方：`Dynamixel_dir is based on Tx`）。若 DIR 一直钉死发送 → 舵机回不来。

### 4.4 接上那只已知好舵机再 Ping

在主机包 **之后** 应再出现 **第二串**（舵机回包），间隔约几十～几百 µs。

| 现象 | 判断 |
|------|------|
| 只有主机包，无回包 | 线序/ID/电压/DIR 不释放；或回包被 getty 吃掉（先做 §3） |
| 有回包，软件仍 timeout | **软件没读到**：getty / 另一进程占口；或 RX 路径 U7 虚焊（总线有波形但 MCU 收不到） |
| 回包幅度塌、毛刺多 | 线太长/接触差；换短 EH 线，只挂 1 只 |
| 回包叠在主机包上 | 半双工冲突：DIR 切太晚或 U6 没高阻 |

对照：同一只舵机 + U2D2，CH1 夹舵机 DATA，应能看到 **问+答**。HAT 只有问没有答 → 硬件/DIR；HAT 有问有答软件仍失败 → §3。

---

## 5. 硬件 PHY（波形不对时）

按 [[hat-solder-kit]] §6.4 核对：

- **必有：** U5、U6、U7、**R29**、C15、R31/R32、J13/J14
- 不用 485：**U8 / J3 / J11 可空**；不要误以为没 U8 就不能 TTL
- J4 40-pin 接触、UART2 对应脚无桥锡

---

## 6. 决策树（短）

1. **U2D2 扫得到这只舵机？** 否 → 修舵机/线/Wizard。
2. `/dev/ttyS2` 在？getty masked？`console=display`？否 → 跑 `setup-board` / 改 `armbianEnv.txt` 后**重启**。
3. 示波器 DATA **有主机包？** 否 → UART / J4 / overlay。
4. **有回包？** 否 → 针序 / DIR / U6 一直驱动 / 电压。
5. 有回包但软件仍失败 → U7（RX）/ 仍有进程占 `ttyS2`。

## 7. 2026-09-16 复测结果（HAT TTL 已打通）

**结论：通了。** 6.0 V 台供 · getty masked · `fuser` 干净 · `console=display`（本次已生效）·
**1 Mbps 全静默 → 57 600 上 ID 1 应答**（model 1200）。舵机仍是**出厂状态**（[[xl330-cn-bench-kit]] 基线表）——
§1.1 的出厂回退是**本次唯一命中路径**，**只按 1 Mbps 测会得到错误的「零回包」结论**。

> **本轮先拿到过一次假阴性**：脚本 CRC 漏了 4 字节 header，`self-test` 的假舵机照抄同一错误 → 自检全绿、台架两档全静默。
> **教训：loopback 自检只证明自洽，不证明合规**。另：状态帧里的 `0x55` 是 **DXL 2.0 的 Instruction 字段**（2026-09-21 定论 → [[dxl-bench-method]] §5.1）。
> 两坑与逐项实测 → [[dxl-bench-method]] §7 · `scripts/README.md`。

## 8. 验收与裁决

验收清单（含主控↔HAT 补充项：**DXL 口是否真上电** · **单变量原则** · **分支定位** · **证据随单**）与 M1–M6 裁决
→ **[[dxl-bench-method]] §6 · §4**。

相关：[[hat-solder-kit]] · [[xl330-cn-bench-kit]] · [[board-interconnect]] · [[zero3w-bench-plan]] · [[dxl-bench-method]]
