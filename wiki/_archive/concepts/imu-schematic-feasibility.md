---
title: imu_to_dxl 原理图用嘉立创 MCP 绘制的可行性
created: 2026-08-30
updated: 2026-08-30
type: concept
tags: [imu, board, open-source]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/articles/jlceda-mcp-hub-readme-2026-08-30.md
confidence: high
related: [imu-to-dxl-v2, jlceda-mcp-setup, opensource-coverage, elec-rpi-robot-hat]
contested: false
---

# imu_to_dxl 原理图 × 嘉立创 MCP：可行性论证

## 结论（先说）

| 目标 | 可否 |
|------|------|
| 用 MCP **辅助画出「功能块级 / 参考」原理图** | **可以**（在 EDA+Bridge 联通后） |
| 用 MCP **还原与量产一致的正式原理图** | **不可以**（公开信息不足） |
| 仅靠 MCP **从零自动生成可流片网表** | **不现实**（Hub 以交互放置为主；关键器件未知） |

## 已知电气事实（公开）

来自软件/文档，非原理图：^[raw/articles/workspace-readme-hardware-2026-08-29.md]

- 传感：[[imu-to-dxl-v2]] → **LSM6DSV16X**（SFLP 四元数）
- 总线：Dynamixel Protocol 2.0 @ ~1 Mbps，**ID 200**，与 [[dynamixel-xl330]] 共线
- 供电：经 [[elec-rpi-robot-hat]] 电机口 **+BATT**（约 NP-F 电压）
- 有 **MCU**（产线 `flash.sh`）；原理图/固件 **未开源**

## 未知（挡住「准确还原」）

- MCU 确切型号与封装（STM32 / CH32 / 其它？）
- IMU 走 SPI 还是 I2C、电平与上拉
- DXL 单线半双工的具体收发电路（开漏/专用 PHY）
- LDO/TVS/ESD、晶振、去耦、连接器型号与位号
- 与 HAT BMI088 的差异只知「alpha 不用板载 BMI」

**没有** PCB 照片、X 光、网表或泄出工程时，任何「完整原理图」都是**猜测**，不能当复刻依据。

## MCP 实际能力边界

见 [[jlceda-mcp-setup]]：官方 Hub 擅长 **读图、选型确认、引导放置**；电源/地需手加；连线自动化弱于 easyeda-mcp-pro。

因此合理用法是：

1. 在嘉立创新建空白原理图页并连上 Bridge  
2. Agent 给出 **块图 BOM**（MCU 占位、LSM6、DXL 3P、3.3V LDO、TVS…）并 `component_select`  
3. 你确认型号后交互放置，再手动画电源/地与关键网  
4. 图上标题明确标注：**Reference / Hypothetical — not official imu_to_dxl**

## 更稳妥的替代路径

| 路径 | 说明 |
|------|------|
| 继续等开源 / 授权 | 唯一「真图」来源 |
| 实物逆向（拍照+测点） | 可提高置信度，再进 EDA |
| 用 **KiCad** 画参考图 | 与已开源 [[elec-rpi-robot-hat]] 工具链一致，不一定非嘉立创 |
| 只画 **系统框图**（本 wiki / Draw.io） | 不冒充原理图 |

## 建议决策

- **要「能聊、能练手、能出参考图」** → 装好 EDA + Bridge，用 Hub 画 **标注为假设** 的块级原理图。  
- **要「能做兼容板」** → 必须补 MCU 选型与 DXL PHY 设计规范，或逆向实物；MCP 只是画图工具，不填知识缺口。

相关：[[imu-to-dxl-v2]] · [[jlceda-mcp-setup]] · [[opensource-coverage]] · [[firmware-flash-matrix]]
