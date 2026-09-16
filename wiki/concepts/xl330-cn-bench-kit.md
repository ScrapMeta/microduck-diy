---
title: XL330-CN 台架测试（国产启动套件）
created: 2026-09-10
updated: 2026-09-11
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

> **状态：✅ 台架已通过（2026-09-10）。** Issue [#1](https://github.com/ScrapMeta/microduck-diy/issues/1)（closed）。详细截图/参数表 **资料后补**。  
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
| 结论 | **通过**（2026-09-10） |
| 范围 | 国产启动套件路径：驱动识别 · 扫舵机 · 冒烟运动 |
| 明细 | **待后补**（端口 / 波特率 / ID / 电压 / 截图等） |

### 勾选（汇总）

- [x] 驱动与 U2D2 识别、扫到舵机、台架冒烟（用户确认通过）
- [ ] 后补：端口名、波特率、ID、电压、固件版本、异常记录与截图

### 实验笔记

#### 2026-09-10

- **结果：** 测试通过。  
- **资料：** 后补。

## 与官方生态的关系

- 台架成功 ≠ 装机完成；装机总线仍须对齐 HAT TTL、ID 图、母线电压策略。  
- CN 组装版与 Robotis 原厂电气契约应同属 XL330-M288 族；若后补资料显示寄存器/固件差异，回写 [[dynamixel-xl330]]。

相关：[[dynamixel-xl330]] · [[diy-milestones]] · [[diy-bom]] · [[bench-power-supply]]
