---
title: 台架供电（无电池）
created: 2026-08-30
updated: 2026-09-16
type: concept
tags: [power]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: high
---

# 台架供电（无电池）

| 场景 | 供电 |
|------|------|
| 仅 [[radxa-zero-3w]] | **5V Type-C**；推荐 Radxa **PD30W** 或 ≥5V/2A（≥15W）优质头 |
| HAT + 舵机 | **勿指望 USB-C**；向 [[elec-rpi-robot-hat]] 电池口供 **6.0 V**（= 整机运行点；**6.0–6.5 V** 为调试可用带），台供 **≥3 A** |

**电压口径已收口（2026-09-16）**：本页原写「7.4–8.4 V」，那是照 NP-F 标称写的。手册 `Input Voltage` **3.7–6.0 V（推荐 5.0 V）**，`Max Voltage Limit(32)` 默认 **70 = 7.0 V**；实测这批 XL330 **~7.2 V 即过压报警**。**台架一律 6.0–6.5 V（6.0 V 优先）。**

> **机制订正（hardware 2026-09-16，据手册 Shutdown 位表）**：过压置 `Hardware Error Status(70)` bit0（Input Voltage Error）；
> 但**是否锁存 torque off 由 `Shutdown(63)` 决定**——**出厂默认 53 含 bit0**，而官方 `robotd` 写的 **52 正好清掉 bit0**。
> 且过压 shutdown 只清 `Torque Enable`、红灯持续闪，**舵机仍应答 Ping/Read** → 是「不动」而非「零回包」。详见 [[dxl-bench-method]] §1.1。

**限流分段（2026-09-16）**：**纯 HAT**（不叠 Zero、不接舵机）**1 A**；**叠 Zero 后 2–3 A**（Zero 启动峰值会超 1 A）。
台供在恒流(CC)触限时是**拉低母线**、不是干净断开 → 限流值**上电前**按当前构型设好，别「先 1 A 再调」（否则 Zero 掉压会假象成「不启动 / 无 `ttyS2`」）。

整机正常路径：[[np-f550-battery]] → HAT → 5V 给 Radxa。**NP-F 直供（6.6–8.4 V）会超舵机上限**，DIY 建议机身加 buck 降到 **6.0 V**（= 整机运行点）再粗线进 HAT，
见 [[body-imu-hat-dxl-power-eval]] §3.1/§5（整机行走峰值预算 **数安以上**，故整机台供按 5–10 A 备）。双供电冲突需小心。

相关：[[board-interconnect]] · [[radxa]] · [[dynamixel-xl330]] · [[body-imu-hat-dxl-power-eval]]
