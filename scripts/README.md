# `microduck-diy/scripts/` — 台架 / 上机脚本

> 可版本化的台架脚本。**规格真源**仍是 `wiki/`；本目录只放能在板上或台架复跑的**代码**。
> 治理见 [`../governance/agent-governance.md`](../governance/agent-governance.md) §5。

## 为什么在这里

`res/`（Dynamixel SDK zip、Wizard 安装包）与 `tmp/` 都**不入库**，且带提取码/网盘，
事后无法核对当时用的是哪套工具与参数 —— Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)
的「以板上已装工具为准」因此**不可复现**。本目录用最小、自带协议实现的脚本取代它。

## `dxl_ping.py` — XL330 只读扫 / Ping / 基线读取

Dynamixel **Protocol 2.0** 只读探针（PING / READ），**不写任何寄存器**（ID / 波特率写入仍归
`robotd` / Wizard）。协议与 CRC 在文件内实现，只依赖 `pyserial`，故没有 SDK 版本漂移。

```bash
pip install pyserial

python scripts/dxl_ping.py self-test                       # 无硬件，自检 codec
python scripts/dxl_ping.py scan  --port COM7               # 1 Mbps 全 ID 扫描（U2D2）
python scripts/dxl_ping.py scan  --port /dev/ttyS2 --baud 1000000,57600
python scripts/dxl_ping.py info  --port COM7 --id 1        # 读基线（ID/波特率/固件/电压/…）
python scripts/dxl_ping.py probe --port COM7 --expect 10,11,12
```

| 子命令 | 作用 |
|--------|------|
| `self-test` | CRC（按位实现 vs 查表实现）、报文往返、坏 CRC 拒收、`shutdown` 位解码 |
| `scan` | 在给定波特率（可逗号串列）逐 ID Ping |
| `info` | 读一个 ID 的基线寄存器，并对照 `robotd` 的期望值 |
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

## 约定

- 新增脚本请自带 `--help` 与无硬件可跑的 `self-test`（本仓无台架时的唯一回归手段）。
- 结果与参数**回写 Issue + wiki**；脚本只保证「怎么跑」，结论仍以 Issue 为准。
