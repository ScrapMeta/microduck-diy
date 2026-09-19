---
title: microduck-replica（社区复刻）
created: 2026-09-19
updated: 2026-09-19
type: entity
tags: [open-source, servo, feetech, diy]
sources:
  - raw/articles/microduck-replica-fanhao375-2026-09-01.md
  - refs/microduck-replica/README.md
  - refs/microduck-replica/software/飞特适配架构.md
confidence: high
related:
  - feetech-hd-1910
  - feetech-scs-bus
  - openmicroduck
  - dynamixel-xl330
  - imu-to-dxl-v2
---

# microduck-replica（fanhao375）

中文社区复刻项目（`fanhao375/microduck-replica`）。

## 与我们的关系：**同一目标，另一条执行器路线**

它**不照抄官方 HAT + XL330**，而是**换掉整套执行器**：15 颗**飞特 HD-1910-C001**
（→ [[feetech-hd-1910]]），走飞特 SCS 总线（→ [[feetech-scs-bus]]），
自画 `imu_to_dxl` 板、自编烧卡脚本、自写网页调试台。

**所以它不是「官方方案的另一份复刻」，而是「官方的飞特版分支」。**
2026-09-18 **15 颗舵机首次上电、能站起来坐下**。

## 对本项目有价值的四样东西

| 产物 | 价值 |
|---|---|
| `docs/飞特资料/` | **飞特官方一手资料的副本**：SCS 协议 v1.0 · SMS/STS 磁编码内存表 v1.1 · 官方十六进制指令生成表。文档站是前端应用、不好存也难检索，它把正文拉成了 Markdown |
| `software/飞特适配架构.md` | 换执行器的**完整改造方案**：接缝分析、寄存器逐项对照、增益 EEPROM 处置、IMU 两条路线、台架验收 0–11 项 |
| `tools/servo-web/` | 网页调试台 + `feetech.py`（约 100 行，不依赖官方 SDK）。可作 `scripts/dxl_ping.py` 的对称参照 |
| `hardware/imu_to_dxl/` | 自画的同功能板（45×22 mm，STM32G031）+ 首板实测（**J4/J5 的 PH 座外壳配不上飞特线头**）——与本项目 [[imu-to-dxl-v2]] 同类工作 |

另：`tools/radxa/` 烧卡脚本、`踩坑记录.md`（Armbian/AIC8800/URT-2 的坑，与本项目 [[zero3w-bench-plan]] 重叠）。

## 立场差异（读它的结论时要记住）

- **供电**：它走 **2S 直供（6.6–8.2 V）**，本项目母线**定案 6.0 V**（降压）。同一颗舵机在不同工作点，扭矩不同
- **它超压吗**：不。HD-1910 原生 4–8.4 V，2S 正当；反而是本项目 6.0 V 属于**保守使用**
- **它的结论**：换 HD-1910 后**策略必须重训**（Kt 是 XL330 的 2.13 倍，动力学不同档）

相关：[[feetech-hd-1910]] · [[feetech-scs-bus]] · [[openmicroduck]] · [[dynamixel-xl330]] · [[imu-to-dxl-v2]]
