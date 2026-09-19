# `microduck-diy/scripts/` — 台架 / 上机脚本 ＋ 机械校验

> 可版本化的台架脚本。**规格真源**仍是 `wiki/`；本目录只放能在板上或台架复跑的**代码**，
> 外加两台守漂移的 linter 与上游版本锁定。规则见 [`../AGENTS.md`](../AGENTS.md)。

## 目录一览

| 文件 | 是什么 |
|---|---|
| `dxl_ping.py` | 台架 DXL **只读**扫 / Ping / 基线（Protocol 2.0 · 零依赖 · 自带 `self-test`） |
| `servo_swap_compare.py` | 换舵机 A/B 对比（**非只读**，须显式 `--setup`） |
| `md_to_pdf.py` | 把一页 wiki 渲染成 PDF（给人看的可发送件） |
| `wiki_lint.py` | wiki 规范：frontmatter · 行数 · 死链 |
| `refs_lint.py` | 仓内引用：反引号与链接里的路径必须存在 |
| `refresh-upstreams.ps1` · `upstreams.lock` | `refs/` 克隆的版本锁定（**`-Fetch` 才联网**） |

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

## `servo_swap_compare.py` — 换舵机 A/B（XL330 vs 候选件）

回答一个具体问题：**换一颗舵机上去，原厂训练结果所依赖的那个执行器还在不在？**
铭牌接近、接口能插、插上能转，都**不能**回答它 —— 克隆件会照转，同时带着另一条摩擦曲线、
更大的齿轮虚位、或一个原厂没有的柔度元件。

判据是**差值之差**：同一条激励分别跑 XL330（基线，其 sim2real gap 已被接受）与候选件，
比两者「偏离指令曲线的样子」像不像。**绝对误差不重要，误差的*形状*才重要。**

刻意做成**开环**（无策略 / 无 MuJoCo / 无 BAM / 无 mjlab）—— 两个好处：
只依赖 `rustypot` + `numpy`（能在 Zero 本机上跑）；且**隔离出执行器**，
而策略在环的测试会把执行器差异与控制器稳定性混在一起。

```bash
python3 scripts/servo_swap_compare.py self-test         # 无硬件

# 1) 基线：台架那台 XL330，电压全程固定
python3 scripts/servo_swap_compare.py record --label xl330 \
    --port /dev/ttyUSB0 --id 1 --setup --vin 6.2 --out xl330.npz
# 2) 候选：换舵机，其余参数逐字不动
python3 scripts/servo_swap_compare.py record --label rd05t \
    --port /dev/ttyUSB0 --id 1 --setup --vin 6.2 --out rd05t.npz
# 3) 结论
python3 scripts/servo_swap_compare.py compare xl330.npz rd05t.npz --baseline xl330
```

**⚠️ 本脚本不是只读的**（与 `dxl_ping.py` 相反）：动态测试必须写
`Operating Mode(11)` / 位置增益 / torque / goal position。因此它**无 `--setup` 拒绝执行**、
逐条打印每次写入、**每个增益读回校验**（固件会静默钳位超范围值，被钳的增益会伪装成动力学差异）、
退出前关 torque。

### 四相激励：不同缺陷在不同激励下现形

| 相 | 激励 | 抓什么 |
|----|------|--------|
| `steps_large` | ±32~80° 阶跃 | 总体动力学、超调、可达带宽 |
| `steps_small` | ±1/2/5/10° 阶跃 | **死区与回差**：小指令直接不动 |
| `ramp_slow` | ±30° 慢三角 | 静摩擦（稳定跟随误差）与黏滞 |
| `reversals_fast` | ±25° 快速反向 | **迟滞**：同一角度从两个方向到达的差 |

### 指标与诊断

| 指标 | 含义 |
|------|------|
| `tracking_mae/rms/max` | 偏离指令的幅度 |
| `dead_time_s` | 指令变化后**覆盖半步**所需时间（弹性元件 / 摩擦变大 = 起步更慢）|
| `dead_steps` | **完全没动**（<指令 20 %）的小步数量 —— 死区最干净的签名 |
| `hysteresis` | 反向到达同一角度的差 |

判定容差 `1.25×` / `2×`（pass / suspect / fail）。`dead_steps` 是**计数**不是倍数：
基线 0、候选若干 = 出现了一个基线没有的死区 → 直接 fail。

**诊断分型**（决定能不能修）：

- 只 `tracking_mae` 大 → 摩擦/电机不同 → **重新辨识摩擦可以救**
- `dead_time` / `hysteresis` / `dead_steps` 也大 → **机械虚位或柔度元件**（过载离合正是这个样子）
  → **重辨识救不了**，任何控制器都消不掉机械虚位

### 两个设计要点

1. **守卫 `Model Number(0)`**：非 1200 时**拒绝执行**，除非显式 `--allow-unknown-model`。
   上游驱动 `duck-control/src/bus.rs` 的 `adopt_replacement` **没有这个守卫** ——
   只要能 Ping + 能写寄存器就会被**静默收养**为关节舵机，失败只会以「走不好」的形式出现。
   本脚本的守卫是刻意补上的。
2. **调度哈希校验**：激励由确定性序列生成并落盘，`compare` 校验两次录音的哈希**完全相同**，
   不一致即**拒绝比较** —— 比错激励得出的「差值之差」比没有结论更糟。

`--duration` 默认 60 s；容差就是按这个长度定的。更短的时长会按比例压缩所有相位
（大步保持时间变短），脚本会打提示，只适合冒烟测管道。

### 先空载跑，别等台架

`dead_steps` / `hysteresis` / `dead_time` 测的是**虚位与柔度**，**空载就能显形**
（输出轴在间隙内的自由行程不需要外力）。只有 `ramp_slow` 的摩擦对比需要配重：
**空载没有力矩，静摩擦几乎不被激励**。

所以：**空载先跑一遍**，只看虚位三个指标，约一小时就能判掉「离合 / 回差」这个
**重辨识也救不了**的风险；通过了再上摆臂做完整版。
**注意空载的 `tracking_mae` 不能用来判摩擦**，只用于判虚位。

分阶安排与「要不要做 BAM 辨识」的决策表见
[`wiki/concepts/bam-identification-bench.md`](../wiki/concepts/bam-identification-bench.md) §「分阶测试」。

### 与上游 `microduck_rl` 的关系

策略在环的问题仍归 [`refs/microduck_rl/scripts/testbench_sim2real.py`](../refs/microduck_rl/scripts/testbench_sim2real.py)
（同一个 ONNX 在 sim 与真机各跑一遍）。把它的 `--mode sim` 轨迹喂进来即可一次拿到两者：

```bash
python3 scripts/servo_swap_compare.py compare xl330.npz rd05t.npz \
    --baseline xl330 --sim sim_trace.npz
```

`self-test` 会交叉核对本脚本的 tick 数与上游 `make_target_schedule` 一致（只读 `refs/`，不改它）。

## `md_to_pdf.py` — 把一页 wiki 渲染成 PDF（给人看的）

wiki 里有一部分内容是**要发出去的**：厂商询问函、给台架上的人看的流程。`.md` 对这类读者是错的形状——
拿到的是原始标记：读不懂的 frontmatter、塌掉的表格、指向他没有的页面的 `[[链接]]`。

```bash
python3 scripts/md_to_pdf.py --check                                  # 报告用哪个浏览器
python3 scripts/md_to_pdf.py wiki/queries/rd05t-vendor-inquiry-2026-09-18.md \
    --exclude-regex '^相关：'                                          # 去掉只在仓内成立的尾行
```

**它只渲染一页，刻意不做静态站点生成器** —— 真源仍是 wiki，这只是一次性导出。
它**剥掉只在仓内成立的东西**（frontmatter、`[[wikilink]]`、以及你点名要删的行），
而**不是**让人再维护一份「可发送副本」：**第二份副本就是会漂移的那份**。

排版用**无头 Chrome/Edge 打印**（本机已有，且无需装 LaTeX 就能处理中文与表格）。
字体栈第一顺位是**真实的 CJK 字体**而非泛化的 `sans-serif` —— 后者可能解析到只有拉丁字形的字体，
中文会渲染成方框，而**这不会体现在退出码里**。故渲染后会**把 PDF 读回来**核对正文是否还在
（无 `pymupdf` 则跳过并说明），同理台架脚本查读回值而不看写入返回值。

```text
退出码 0 只代表「Chrome 退出了」。本脚本判成功看的是**文件真的在、且文字真的能读回**——
因为 Chrome 对相对 Windows 路径会报 "cannot find the path specified" **同时仍然返回 0**。
```

> **约定豁免（唯一一个）**：本节约定要求「无硬件可跑的 `self-test`」，本工具**没有**——
> 它的前置条件不是硬件而是**浏览器**，故以 `--check` 声明前置条件。它是唯一非台架脚本。

### 产物放哪

PDF 与源 `.md` **同级**（如 `wiki/queries/rd05t-vendor-inquiry-2026-09-18.md` → 同名 `.pdf`），因为它就是要发出去的那份。
它是**派生物**：源改了要**重新生成**，不要手工编辑 PDF。中间 HTML 默认不落盘（`--keep-html` 可留）。

## 两台 linter —— 守「别漂」（2026-09-19 加）

规则在 [`../AGENTS.md`](../AGENTS.md)，**机械校验在这两台脚本** —— 它们抓的是人不会主动发现的那类漂移：
页面改了名、规则搬了家，但别处还写着老路径。

```bash
python3 scripts/wiki_lint.py     # frontmatter · 行数 · 死链
python3 scripts/refs_lint.py     # 反引号 / 链接里的仓内路径是否存在
python3 scripts/lint_selftest.py # 上面两台的自检：注入故障，必须报错
```

- **`wiki_lint.py`** —— 正文页必须有 frontmatter（`title` `created` `updated` `type` `tags`）· **≤ 200 行** ·
  `[[name]]` 形式的 wikilink 与相对 `.md` 链接必须解析得到。
  豁免：`raw/` `_archive/` `assets/` **整体跳过**（改它们的链接等于篡改历史记录）·
  `index` / `log` / `tasks` 免 frontmatter 与行数 · **`log.md` 另免死链**（只追加的流水，历史链接不该回溯失效）·
  超长页分两类：**没记账的 → error 要求拆页**；`OVERSIZE_ACK` 里的 = **已批准的例外（不拆页 · 对外可发送件 / 对比页）**，
  其数值**只减不增**（超记账值即 error，降到 ≤200 行提示删条目；批准出处见该文件内的注释）。
- **`refs_lint.py`** —— 扫反引号与 markdown 链接里**指向本仓**的路径。判据分两层：
  1. **哪些像仓内路径**：首个路径段要命中 `root_entries() ∪ KNOWN_PREFIXES`。
     `KNOWN_PREFIXES` 收**历史前缀** —— 否则「整个目录被删 / 改名」这类**最该抓**的漂移反而会放行
     （本仓实例：旧治理层搬走后，指向它的老引用本该报错）。只收**无歧义**的旧前缀：
     `docs` 刻意不收，因为本仓多处 `docs/…` 指的是*别的仓*里的 docs，收进来立刻一片假阳性。
  2. **缺席是否合法**：只看 `LOCAL_ONLY_PREFIXES` 一张显式表，**刻意不用 `git check-ignore`**
     —— 它的判定随「索引里有没有东西」而变，实测在空仓里会把每条路径都判成 ignored，
     于是所有引用被静默放行。新增被 ignore 的目录时，这张表和 `.gitignore` **两处一起改**。
- **`lint_selftest.py`** —— **校验器自己也要能被证伪**。克隆仓库到 `temp/`，种下已知故障，
  断言两台 linter 都真的报错；再撤掉故障，断言干净克隆全绿。一台「永远 exit 0」的 linter
  和没有 linter 一样，但看起来更有保障 —— 这一步就是防这个。
  2026-09-19 首次跑它就抓出 `refs_lint` 的两个真 bug（都只在注入故障时才会暴露）。

CI（`.github/workflows/ci.yml`）在 push / PR 到 `main` 时跑这三条。
**改脚本的参数（`MAX_LINES` · `SKIP_DIRS` · `TARGET_GLOBS` · `LOCAL_ONLY_PREFIXES` · `KNOWN_PREFIXES` …）
等于改规格**，先读 `AGENTS.md` 的改法表。

### 在开发机（Windows）上怎么调

宿主工具链实况（Git 版本下限 · `python` / `python3` / `py` 各自解析到谁 · PATH 顺序）记在
[`wiki/concepts/local-workspace-layout.md`](../wiki/concepts/local-workspace-layout.md) §「宿主工具链」。

两个要点：**这两台只用 stdlib，下限 Python 3.9**，别给它们加依赖；
开发机上 **`python3` 仍是商店占位符**（报 not found），用 `python`（3.12）或 `py -3.12` 调。

## 约定

- 新增**台架**脚本请自带 `--help` 与无硬件可跑的 `self-test`（本仓无台架时的唯一回归手段）；
  非台架工具用 `--check` 声明前置条件（目前仅 `md_to_pdf.py`）。
- 结果与参数**回写 wiki**（`wiki/log.md` ＋ 对应页）；脚本只保证「怎么跑」，结论以 wiki 为准。
- 会写总线的脚本必须在**文件名或文档里明示非只读**，并给出 `--setup` 之类的**显式开关**：
  本仓的默认预期是「探针只读」。

