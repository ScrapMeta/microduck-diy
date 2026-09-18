# `microduck-diy/scripts/` — 台架 / 上机脚本

> 可版本化的台架脚本。**规格真源**仍是 `wiki/`；本目录只放能在板上或台架复跑的**代码**。
> 治理见 [`../governance/agent-governance.md`](../governance/agent-governance.md) §5。

## 为什么在这里

`res/`（Dynamixel SDK zip、Wizard 安装包）与 `tmp/` 都**不入库**，且带提取码/网盘，
事后无法核对当时用的是哪套工具与参数 —— Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)
的「以板上已装工具为准」因此**不可复现**。本目录用最小、自带协议实现的脚本取代它。

## `dxl_ping.py` — XL330 只读扫 / Ping / 基线读取

Dynamixel **Protocol 2.0** 只读探针（PING / READ），**不写任何寄存器**（ID / 波特率写入仍归
`robotd` / Wizard）。协议与 CRC 在文件内实现；**在 Linux 上零依赖**（有 `pyserial` 就用，没有就退回
stdlib `termios` —— 板子 `python3` 常既无 `pyserial` 也无 `pip`，要求装包会让流程在目标机上跑不起来）。

```bash
python3 scripts/dxl_ping.py self-test                      # 无硬件，自检 codec
python3 scripts/dxl_ping.py scan  --port COM7               # 1 Mbps 全 ID 扫描（U2D2）
python3 scripts/dxl_ping.py scan  --port /dev/ttyS2 --baud 1000000,57600
python3 scripts/dxl_ping.py info  --port COM7 --id 1        # 读基线（ID/波特率/固件/电压/…）
python3 scripts/dxl_ping.py probe --port COM7 --expect 10,11,12
```

| 子命令 | 作用 |
|--------|------|
| `self-test` | CRC（按位实现 vs 查表实现）、**公开报文向量**、报文往返、坏 CRC 拒收、非标准帧回放、`shutdown` 位解码、`Operating Mode(11)` 解码 |
| `scan` | 在给定波特率（可逗号串列）逐 ID Ping |
| `info` | 读一个 ID 的基线寄存器（含 **`Operating Mode(11)`**），并对照 `robotd` 的期望值 |
| `probe` | 复刻官方探测顺序：预期 ID @ **1 Mbps** → 若恰一个缺失，探出厂舵机 **ID 1**（先 1 Mbps，再 **57 600**）|

**基线采集**：`info` 的输出即 Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) / `wiki/concepts/xl330-cn-bench-kit.md`
所需的「ID / 波特率 / 固件 / 当时电压」。贴原始命令与输出，勿手工转写。

**只读边界**：本脚本刻意**不含**写 ID / 写波特率 / 寄存器修正。

```text
robotd 的适配路径（本脚本只打印、不执行）：
  写缺失 ID → 写 baud_rate → 重开 1 Mbps → 查寄存器
  (return_delay_time=0 · baud_rate=3 · pwm_slope=255 · shutdown=52) → 重启舵机
```
重启用于**清除烧写留下的锁存 hardware-error**，否则 torque 保持关闭。

## 两个已踩过的坑（2026-09-16 台架实测 · Issue #4）

### 1. CRC 必须覆盖 4 字节 header

CRC-16/IBM 的作用域是「从 `FF FF FD 00` 起到最后一个参数」，**不是**从 ID 起。
早期版本漏了 header，`self-test` 的假舵机**照抄了同一个错误**，所以自检**全绿**、
第一次台架扫描却**两档波特率全「无回包」** —— 报文根本没被舵机接受。
现在 `self-test` 用公开向量 `ff ff fd 00 01 03 00 01 19 4e`（ID 1 的 PING）钉死作用域。
**教训**：loopback 自检只能证明收发两端一致，不能证明符合规格；必须拿公开向量做锚。

### 2. 本套件的舵机回包多一个固定字节

台架这台（XL330-CN 套件）的状态帧是 `HEADER · ID · LEN · 0x55 · ERROR · DATA · CRC`，
`LEN = len(DATA) + 4`（规格是 `+ 3`）。**0x55 在线上、且被舵机自己的 CRC 覆盖**，
不是本脚本读错：若它只是本地串口噪声，`want` 与 `got` 就不会 14/14 全等。
按规格解析会得到 `error=0x55` 且**每个寄存器整体错位一字节** —— 值看着都像对的，
其实全是「合理但错误」的数（`model=45056`、`max_voltage_limit=1792.0 V`）。
脚本按**「PING 应回 3 字节 / READ 应回请求长度」**这两个已知长度自动判别两种帧，
并在 `-v` 下打印提示；`self-test` 用实测原始帧做回放回归。

> 该字节的**来源未定论**（单位固件怪癖 vs 其它）。交叉验证办法：同一只舵机接 **U2D2 +
> Dynamixel Wizard** 看是否同样存在 —— Wizard 是独立实现，能一锤定音。

## 为什么 `info` 也读 `Operating Mode(11)`（2026-09-18）

XL330 有**两个**输出限幅，**不是每个模式都同时生效**：

| 寄存器 | 默认 | 生效范围 |
|--------|------|----------|
| `PWM Limit(36)` | 885 = 100 % | **所有**模式 |
| `Current Limit(38)` | 1750 = 1.75 A | 仅 **Current Control(0)** 与 **Current-based Position(5)** |

出厂默认模式是 **3 = Position Control**，此时 `Current Limit(38)` **不生效** ——
「电流被 1.75 A 钉住」这个常见假设**在默认模式下是错的**：母线升压会让输入电流超出
6.0 V 额定（1.74 A）而**不受该寄存器保护**。

`Operating Mode(11)` 决定该用哪条结论，而 `robotd` **不写**这个寄存器（只写
`return_delay_time` / `baud_rate` / `pwm_slope` / `shutdown`），所以只能读出来。
见 [`wiki/entities/dynamixel-xl330.md`](../wiki/entities/dynamixel-xl330.md) §「母线电压天花板」。

## 约定

- 新增脚本请自带 `--help` 与无硬件可跑的 `self-test`（本仓无台架时的唯一回归手段）。
- 结果与参数**回写 Issue + wiki**；脚本只保证「怎么跑」，结论仍以 Issue 为准。
