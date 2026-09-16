---
title: XL330-CN 台架测试（国产启动套件）
created: 2026-09-10
updated: 2026-09-16
type: concept
tags: [servo, dynamixel, procurement, diy]
sources:
  - raw/articles/xl330-cn-starter-kit-notes-2026-09-10.md
confidence: high
related:
  - dynamixel-xl330
  - diy-bom
  - diy-milestones
  - robotis-xl330-order-2026-09-05
  - bench-power-supply
  - board-interconnect
---

# XL330-CN 台架测试（国产启动套件）

> **状态：✅ 台架已通过（2026-09-10）。** Issue [#1](https://github.com/ScrapMeta/microduck-diy/issues/1)（closed）。
> **基线明细：证据不足**（2026-09-16 复核，从未记录）→ 见下「基线参数」· 复测前用 `scripts/dxl_ping.py` 采集。  
> 规格真源：[XL330-M288 eManual](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/) · 实体 [[dynamixel-xl330]]

## 到货 / 在用硬件

| 项 | 说明 |
|----|------|
| 舵机 | **XL330-M288-T-CN**（国内组装版） |
| 适配器 | 国产 **U2D2** |
| 电源板 | 国产 **PHB**（启动套件） |
| 电源 | 国产电源（台架） |

与整机路径区别：本页是 **PC ↔ U2D2/PHB ↔ 舵机** 冒烟；整机仍是 [[elec-rpi-robot-hat]] + 电池母线（见 [[board-interconnect]]）。官方 Robotis 直邮单见 [[robotis-xl330-order-2026-09-05]]（可并存）。

## 软件与 SDK

| 项 | 链接 | 提取码 |
|----|------|--------|
| Windows 驱动 | https://pan.baidu.com/s/18OJQQWEFEVYN_M_cbFGI5Q | `eqvs` |
| Linux 驱动 | https://pan.baidu.com/s/1hMBkdQxxtTyO50kUlH1FfA | `e79f` |
| Dynamixel SDK | https://pan.baidu.com/s/1bF0tRPhxrAExfsroCGx5pA | `1146` |

## 教程

| 内容 | 链接 |
|------|------|
| 智能佳 XM430 + 国产 U2D2 + PHB（原理同国产启动套件） | https://b23.tv/tJ46kfE · [BV1voqwYAEEo](https://www.bilibili.com/video/BV1voqwYAEEo) |
| XL330 + 进口 U2D2（对照；国产套件原理一样） | 同上 BV |

## 测试结论

| 项 | 结果 |
|----|------|
| 结论 | **通过**（2026-09-10，用户口述确认） |
| 范围 | 国产启动套件路径：驱动识别 · 扫舵机 · 冒烟运动 |
| 明细 | **未记录**（见下） |

### 基线参数（M3）· 2026-09-16 复测**已采集**

`#1` 的基线**从未落到任何真源**（wiki / `raw/` / `temp`·`res` / 会话都查不到）→ 本轮不再等 #1，
改为**直接在 HAT 总线上采集**（`/dev/ttyS2 @ 57 600`，`scripts/dxl_ping.py info`，2026-09-16）：

| 字段 | 实测值 | 与手册出厂默认 |
|------|--------|----------------|
| Model Number | **1200** | ✅ XL330-M288 |
| Firmware Version | **53** | — |
| ID | **1** | ✅ 出厂 1 |
| Baud Rate(8) | **1 → 57 600** | ✅ 出厂 1 |
| Return Delay Time(9) | **250** | ✅ 出厂 250 |
| Max Voltage Limit(32) | **70 → 7.0 V** | ✅ 出厂 70 |
| Min Voltage Limit(34) | **35 → 3.5 V** | ✅ 出厂 35 |
| PWM Limit(36) | **885** | ✅ 100% |
| Current Limit(38) | **1750 → 1.75 A** | — |
| PWM Slope(62) | **140** | ✅ 出厂 140 |
| Shutdown(63) | **53** | ✅ 出厂 53（**含** InputVoltage 位） |
| Torque Enable(64) | **0** | 台架正常（未使能） |
| Status Return Level(68) | **2** | ✅ |
| Hardware Error Status(70) | **0** | ✅ 无故障 |
| Present Input Voltage(144) | **58 → 5.8 V** | 台供 6.0 V 下 |
| Present Temperature(146) | **26 °C** | — |

**结论性事实：**

1. 这台舵机**仍是出厂状态**（ID 1 + 57 600 + 全部默认值未被写过）→ **#1 的「1 Mbps + 同一颗」前提不成立**：
   它从未被 `robotd`/Wizard 写过 ID 或波特率。以前能"通过"，只可能是 Wizard 自动扫到了 57 600。
2. **只有 57 600 有回包**；**1 Mbps 全程静默** → 与 `[[dxl-bench-method]]` §2 的出厂回退一致，
   也再次证明**只按 1 Mbps 测必得假「零回包」**。
3. `Shutdown = 53` 实测到手，**直接证实** [[dynamixel-xl330]] 的订正：出厂 53 **含** Input Voltage 位，
   `robotd` 写的 52 才是**清掉**它。`Hardware Error Status = 0` + 5.8 V 说明本机没过压、通信正常。
4. `Current Limit = 1750 (1.75 A)` 实测值可作 [[dxl-bench-method]] 台供限流的参照。

> ⚠ 回包帧**多一个固定字节 `0x55`**（`LEN = DATA + 4`），按规格解析会把每个寄存器整体错位一字节。
> 见 `scripts/README.md` §「两个已踩过的坑」· [[dxl-bench-method]] §5。

### 复采命令

```bash
python3 scripts/dxl_ping.py info --port /dev/ttyS2 --baud 57600 --id 1
python3 scripts/dxl_ping.py scan --port /dev/ttyS2 --baud 1000000,57600
```

`info` 一次给全上表；脚本**只读、不写**，在 Linux 上零依赖（无 `pyserial` 时走 stdlib `termios`）。
落点：[[hat-dxl-bus-debug]] §1 · [[dxl-bench-method]] · `scripts/README.md`。

### 勾选（汇总）

- [x] 驱动与 U2D2 识别、扫到舵机、台架冒烟（用户确认通过）
- [x] **基线采集**：见上表（2026-09-16，HAT 总线采集；ID/波特率/固件/电压齐全）

### 实验笔记

#### 2026-09-10

- **结果：** 测试通过（用户口述）。  
- **资料：** 未留存；2026-09-16 复核确认**无法从聊天/仓库重建**。

#### 2026-09-16（复测 · HAT 总线）

- **基线已采集**（见上表）：该舵机**仍出厂状态**（ID 1 / 57 600 / 默认寄存器），**从未被写过 ID 或波特率**。
- 复测同时暴露**脚本 CRC 作用域 bug**（漏掉 4 字节 header）与**回包多一固定字节**两个坑，
  详见 `scripts/README.md` §「两个已踩过的坑」；已修 + 已加回归。

## 与官方生态的关系

- 台架成功 ≠ 装机完成；装机总线仍须对齐 HAT TTL、ID 图、母线电压策略。  
- CN 组装版与 Robotis 原厂电气契约应同属 XL330-M288 族；若后补资料显示寄存器/固件差异，回写 [[dynamixel-xl330]]。

相关：[[dynamixel-xl330]] · [[diy-milestones]] · [[diy-bom]] · [[bench-power-supply]]
