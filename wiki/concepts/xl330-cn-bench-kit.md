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

### 基线参数（M3 · 2026-09-16 复核：**证据不足**）

Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) 的前提是「**同一颗** U2D2 已验证的舵机」，
但 #1 的基线**从未落到任何真源**：wiki / `raw/` / 本机 `temp`·`res` / agent 会话里都**查不到**实测的
**ID / 波特率 / 固件 / 当时电压**。按治理「**聊天不算**」，此处**不臆造**，据实标为**证据不足**。

| 字段 | 值 | 来源 |
|------|-----|------|
| 端口 | 未记录 | — |
| ID | 未记录（出厂默认 = **1**，未回读） | — |
| 波特率 | 未记录（出厂默认 = **1 → 57 600**，未回读） | — |
| 固件版本 | 未记录 | — |
| 当时电压 | 未记录 | — |
| 已知（构造性） | XL330-M288-**T-CN** · 国产 U2D2 + PHB · 台架自供电源 · **单只** | raw |

> **缺口不可忽略**：#4 的「同一颗舵机 + 1 Mbps」**没有可核对的基线**，
> 且**只按 1 Mbps 测会漏掉出厂 57 600**（[[hat-dxl-bus-debug]] §1.1）。
> 复测前**先采集**下列基线，原始命令与输出贴回 Issue，再写回本页。

### 采集方法（复测时执行）

```bash
pip install pyserial
python microduck-diy/scripts/dxl_ping.py info --port COM7 --id <当前ID>   # 读基线
python microduck-diy/scripts/dxl_ping.py scan --port COM7 --baud 1000000,57600
```

`info` 一次给全：ID / 波特率 / 固件版本 / Max·Min Voltage Limit / Return Delay Time / PWM Slope / Shutdown / 当时输入电压 / 温度。
脚本**只读、不写**，自带无硬件 `self-test`。落点：[[hat-dxl-bus-debug]] §1 · `scripts/README.md`。

### 勾选（汇总）

- [x] 驱动与 U2D2 识别、扫到舵机、台架冒烟（用户确认通过）
- [ ] **基线采集**：端口名、波特率、ID、电压、固件版本（用上述脚本；#4 复测前完成）

### 实验笔记

#### 2026-09-10

- **结果：** 测试通过（用户口述）。  
- **资料：** 未留存；2026-09-16 复核确认**无法从聊天/仓库重建**。

## 与官方生态的关系

- 台架成功 ≠ 装机完成；装机总线仍须对齐 HAT TTL、ID 图、母线电压策略。  
- CN 组装版与 Robotis 原厂电气契约应同属 XL330-M288 族；若后补资料显示寄存器/固件差异，回写 [[dynamixel-xl330]]。

相关：[[dynamixel-xl330]] · [[diy-milestones]] · [[diy-bom]] · [[bench-power-supply]]
