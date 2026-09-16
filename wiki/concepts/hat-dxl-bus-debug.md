---
title: HAT TTL 舵机测不通排查
created: 2026-09-14
updated: 2026-09-16
type: concept
tags: [hat, dynamixel, bench]
sources:
  - concepts/hat-solder-kit.md
  - concepts/xl330-cn-bench-kit.md
  - microduck/scripts/setup-board.sh
confidence: high
related:
  - hat-solder-kit
  - board-hat
  - board-interconnect
  - xl330-cn-bench-kit
  - dynamixel-xl330
  - zero3w-bench-plan
---

# HAT TTL 舵机测不通排查

> 针对：**U2D2 台架曾通过**，叠 [[elec-rpi-robot-hat]] + Zero 后扫不到 / timeout。  
> Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)（v0.1 · 等台架设备）。  
> 工装：**双通道示波器** + **30 V / 10 A 可调电源**（电流可限）。  
> 焊接/485：[[hat-solder-kit]]。接线：[[board-interconnect]]。

官方 `setup-board.sh` 写过同一症状：`read return_delay_time on 20: Operation timed out`，舵机在 U2D2 上正常——**getty 把回包读走了**。

## 0. 台供与只接 1 只舵机

> **母线电压 6.0–6.5 V（pm 定案 2026-09-16；本页原写 7.4 V）。**
> 依据：XL330 手册工作区 **3.7–6.0 V**（控制表默认 Max Voltage Limit ≈ **7.0 V**）；DIY 实测（2026-09-15）
> **~7.2 V 红灯持续闪（过压报警）**，~6.5 V 上电闪一下后正常。
> 且官方 `robotd-design` §2.1：`shutdown=52` 错误掩码**锁存 input-voltage fault 并保持 torque off** ——
> **用错电压本身就会造出「零回包」**，与本单症状同名，勿再当成通信问题查。
> J13/J14 针2 **就是 `+BATT`**、**舵机不经 buck**，故台供电压 = 舵机电压。
> 详见 [[dynamixel-xl330]] · [[body-imu-hat-dxl-power-eval]] §3.1。

| 项 | 设定 |
|----|------|
| 电压 | **6.0–6.5 V**（**勿**用 7.4 V 直供舵机） |
| 电流限 | **纯 HAT 阶段 1 A**；**叠 Zero 后放到 2–3 A** |
| 进电 | J13 或 J14：**针1=GND · 针2=+BATT**；针3 先空 |
| 禁止 | >6.5 V 直供舵机、30 V、Type-C 与 `+BATT` 同时灌、一次挂多只 |

针脚：**1=GND · 2=VBATT · 3=DATA**（与部分飞特线序相反）。

---

## 1. 先证明舵机还活着（绕开 HAT）

用已通过的 [[xl330-cn-bench-kit]]：**PC → U2D2/PHB → 同一只 XL330**。

| 结果 | 含义 |
|------|------|
| U2D2 能扫到 | 舵机/线/ID/波特率 OK → 问题在 **HAT / Zero / 软件** |
| U2D2 也扫不到 | 先修舵机电源、线序、ID、Wizard 波特率（**1 Mbps** · Protocol **2.0**） |

记下：**ID、波特率、固件**。后面 HAT 必须用同一套。

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
| `/dev/ttyS2` 存在 | 无则 overlay：`overlay_prefix=rk3568` + UART2 overlay（`setup-board.sh`） |
| `fuser` | **不能**是 `agetty` / `getty` |
| getty | 必须 **masked**（只 disable 会被 `getty.target` 拉回来） |
| `console=` | 必须 **`display`**，不能是 `both` / `serial`（内核 printk 会打坏回包） |

修完重启再扫。未跑 `provision` / `setup-board.sh` 时，上面几乎必挂。

扫总线（示例；以板上已装工具为准）：

- 官方栈：`robotd` / 仓库自带 ping  
- 或 Dynamixel Wizard / SDK：端口 **`/dev/ttyS2`**，**1 000 000**，Protocol **2.0**

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

```
U2D2 扫得到这只舵机？
  否 → 修舵机/线/Wizard
  是 → /dev/ttyS2 在？getty masked？console=display？
         否 → 跑 setup-board / 手改 armbianEnv 后重启
         是 → 示波器 DATA 有主机包？
                否 → UART/J4/overlay
                是 → 有回包？
                       否 → 针序/DIR/U6 一直驱动/电压
                       是 → U7/RX 或仍有进程占 ttyS2
```

## 7. 本轮验收

- [ ] U2D2 仍能扫到该舵机  
- [ ] HAT 针2 = 台供（**6.0–6.5 V**）；限流未顶死（纯 HAT 1 A；叠 Zero 2–3 A）  
- [ ] getty masked · `console=display` · `fuser` 干净  
- [ ] 空闲 DATA≈3.3 V；Ping 有主机包  
- [ ] 接舵机后有回包，软件能读 ID  

### 7.1 复查补充（2026-09-16 · 主控↔HAT DATA 未打通）

- [ ] **DXL 口是否真的上电** —— 针2 有压 ≠ 舵机口有压；先量舵机座子电压再谈通信  
- [ ] **单变量原则** —— 换线/换舵机/换供电策略一次只动一个，评论里写明本次变量  
- [ ] **分支定位（必须给结论）** —— ①供电未使能 ②串口被占用 ③物理层/方向脚 ④收发器或焊点 ⑤软件配置；证据不足也要写明  
- [ ] **证据随单** —— pin2 电压 · pin3 空闲电平 · ping 主机包与回包波形 · 软件 ping/read ID 输出  

相关：[[hat-solder-kit]] · [[xl330-cn-bench-kit]] · [[board-interconnect]] · [[zero3w-bench-plan]]
