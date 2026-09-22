---
title: 台架供电（无电池）
created: 2026-08-30
updated: 2026-09-22
type: concept
tags: [power]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: high
---

# 台架供电（无电池）

| 场景 | 供电 |
|------|------|
| 仅 [[radxa-zero-3w]] | **5V Type-C**；推荐 Radxa **PD30W** 或 ≥5V/2A（≥15W）优质头 |
| HAT + 舵机 | **勿指望 USB-C**；向 [[elec-rpi-robot-hat]] 电池口供 **6.0 V**（**6.0–6.5 V** 为调试可用带），台供 **≥3 A** —— 「= 整机运行点」的旧依据见下（**2026-09-22 已失效**） |

**电压口径已收口（2026-09-16）**：本页原写「7.4–8.4 V」，那是照 NP-F 标称写的。手册 `Input Voltage` **3.7–6.0 V（推荐 5.0 V）**，`Max Voltage Limit(32)` 默认 **70 = 7.0 V**；实测这批 XL330 **~7.2 V 即过压报警**。**台架一律 6.0–6.5 V（6.0 V 优先）。**

**装机口径改定（Human 2026-09-22 · 已确认定案）**：**降压模块不要了 · 全部退掉** → 装机走**官方 2S 直供**（[[np-f550-battery]] → HAT `+BATT`，**没有 6 V 那一级**）；舵机侧**按官方方案关掉过压锁**（清 `Shutdown(63)` bit0，见 [[dynamixel-xl330]] §「母线电压天花板」）。**7.4 V 上电实测正常 · 未上电池** → 满电 **8.4 V 未验**。2026-09-18「机身降压模块稳 6.0 V 长期运行」的定案**就此作废**。
> **本页只改硬件域**：其余页（[[index]] 焦点 / 优先级 · `tasks.md` 目标行 · [[diy-milestones]] · [[dxl-bench-method]] §1 的依据 · [[bam-identification-bench]] 辨识电压 · [[rd05t-vendor-inquiry-2026-09-18]] C 节 · [[microduck-replica]] 对比）的同步**已归中立会话收口**（Human 2026-09-22 分派）—— 未收口前那些页仍是 6.0 V 口径，**别当成现行**。
> **台架口径是否跟着变 = 未定（待 Human）**：本页上表与 [[dxl-bench-method]] §1 现在仍写 **6.0 V ＋ 限流分段**，那是按「整机 6.0 V」定的；整机换 2S 后，**台架继续 6.0 V 还是随整机走 7.4 V** 两说都通 —— **它同时决定 BAM 的辨识电压**（[[bam-identification-bench]]），故并入同一项口径决定，**本页不擅自改数**。

> **机制订正（hardware 2026-09-16，据手册 Shutdown 位表）**：过压置 `Hardware Error Status(70)` bit0（Input Voltage Error）；
> 但**是否锁存 torque off 由 `Shutdown(63)` 决定**——**出厂默认 53 含 bit0**，而官方 `robotd` 写的 **52 正好清掉 bit0**。
> 且过压 shutdown 只清 `Torque Enable`、红灯持续闪，**舵机仍应答 Ping/Read** → 是「不动」而非「零回包」。详见 [[dxl-bench-method]] §1.1。

**限流分段（2026-09-16）**：**纯 HAT**（不叠 Zero、不接舵机）**1 A**；**叠 Zero 后 2–3 A**（Zero 启动峰值会超 1 A）。
台供在恒流(CC)触限时是**拉低母线**、不是干净断开 → 限流值**上电前**按当前构型设好，别「先 1 A 再调」（否则 Zero 掉压会假象成「不启动 / 无 `ttyS2`」）。

整机正常路径：[[np-f550-battery]] → HAT → 5V 给 Radxa。**NP-F 直供（6.6–8.4 V）超舵机手册上限 6.0 V** —— 2026-09-18 的对策是机身加 buck 降到 **6.0 V** 再粗线进 HAT，**该 buck 已于 2026-09-22 全退**，现按**官方方案直供**（舵机不锁过压；代价 = **再无过压保护** ＋ 满电 8.4 V 未实机验）。
见 [[body-imu-hat-dxl-power-eval]] §3.1/§5（整机行走峰值预算 **数安以上**，故整机台供按 5–10 A 备）。双供电冲突需小心。

相关：[[board-interconnect]] · [[radxa]] · [[dynamixel-xl330]] · [[body-imu-hat-dxl-power-eval]]
