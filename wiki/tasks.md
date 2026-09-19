---
title: 任务台账
created: 2026-09-19
updated: 2026-09-19
type: index
tags: [index, workspace]
---

# 任务台账

> **取代 GitHub Issue** —— 历史 Issue #1–#11 与 Milestone `v0.1` 已冻结只读（见 [AGENTS.md](../AGENTS.md)「GitHub」）。
> 一行 = 一件事。开工改「状态」，收工在 [`log.md`](log.md) 追加一条。
> 阶段验收口径仍看 [[diy-milestones]]；本页只记「当前欠什么」。

## 进行中

| 任务 | 角色 | 验收 | 出处 |
|---|---|---|---|
| HAT TTL：写总线值 ＋ `0x55` 帧异常定论 | `/microduck-hardware` | ① U2D2 ＋ Dynamixel Wizard 交叉验证 `0x55` 来源，**附原始帧**（有 / 无都算结论）② 写 ID / 波特率后在 **1 Mbps** 复验 ③ 示波器：空闲 DATA ≈ 3.3 V · host 包 · 应答包 ④ 限流分级 ＋ 针2 / 5 V / 3V3 实测 | 原 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11) · [[hat-dxl-bus-debug]] · [[dxl-bench-method]] |

## 待办

| 任务 | 角色 | 验收 | 出处 |
|---|---|---|---|
| 拆页：3 页超 200 行上限 | `/microduck-pm` 收口 · 内容归 `/microduck-hardware` | `hat-solder-kit` **399** → 3 页（配料/DNP · 焊接工艺 · 分步测试）· `xl330-vs-kpower-rd05t` **220** → 2 页（事实层 · 判断层）· `rd05t-vendor-inquiry` **203**（对外可发送件 —— 拆前先定「单页件是否该有例外」）。**只减不增**：记账表在 `scripts/wiki_lint.py` 的 `OVERSIZE_ACK`，拆完从表里删掉 | 治理改造 2026-09-19 |
| replica0908 焊接 ＋ U2D2 冒烟（对照 #7 零回包） | `/microduck-hardware` | MCU＋PHY＋电源＋DXL 座＋SWD 可贴完 · CubeProgrammer 能下载 · Ping / Read 结果写清「有回包 / 仍零回包」· 与 #7 对照一句话 | 原 [#8](https://github.com/ScrapMeta/microduck-diy/issues/8) · [[microduck-replica]] |
| 结构可干装配 | `/microduck-structure` | 打印件 / 紧固件 / 轴承 / XL330 装得上 · 件数进 [[mechanical-bom-rl]] | v0.1 未勾项 |
| 电控联调：Zero ＋ HAT ＋ 机身 IMU | `/microduck-software` | [[board-imu-to-dxl]] · [[imu-to-dxl-v2]] 可实施 | v0.1 未勾项 |
| 契约对齐：DXL / IMU / 策略接口与官方生态一致 | `/microduck-software` | [[opensource-coverage]] 无未决缺口 | v0.1 未勾项 |
| RD05T 问询函发出 ＋ 回函落 wiki | `/microduck-hardware` | [[rd05t-vendor-inquiry-2026-09-18]] 已发出（PDF 同目录）· 回函结论进 [[xl330-vs-kpower-rd05t]] | log 2026-09-18 |
| 回收上游 `microduck-replica` 那 9 个提交 | `/microduck-software` ／ `/microduck-hardware` | 飞特官方内存表升为**厂商一手**（订正 [[xl330-vs-feetech-servos]]）· 网页舵机调试台 · imu_to_dxl 首板 PH 座实测（J4/J5） | log 2026-09-19 |
| 喇叭出声孔 · ToF breakout 外形：实测 | `/microduck-structure` | 实测值写回 [[hat-solder-kit]] §6.3 · [[vl53-tof]]（当前均标「查不出，不猜」） | log 2026-09-19 |

## 已完成（近 30 天）

| 任务 | 结论 | 落点 |
|---|---|---|
| 机身 IMU v0.3 固件 P0 修复 ＋ U2D2 验收 | Ping/Read 1000 · SyncRead 10 min 无超时（`a49a628`） | [[imu-to-dxl-firmware-build]] · 原 #10 |
| 机身 6 V 经 DXL 回灌 HAT 评估 | **不采用** —— 电池经降压模块稳在 6.0 V 长期运行 | [[body-imu-hat-dxl-power-eval]] · 原 #9 |
| HAT TTL 舵机 bring-up | **已打通**：出厂 ID 1 @ 57 600 应答复现 · 基线已采集 | [[hat-dxl-bus-debug]] · [[xl330-cn-bench-kit]] · 原 #4 |
| Zero 3W P1 相机台架 | probe `0x0219` · `/dev/video0` 可抓 NV12 | [[imx219-camera]] · 原 #5 |
| HAT 配料焊接 | 首板完成（DNP 项已省） | [[hat-solder-kit]] · 原 #3 |
| Zero 3W P0 系统台架 | flash / boot / SSH 通过 | [[zero3w-bench-plan]] · 原 #2 |
| XL330-CN 舵机台架冒烟 | 通过（2026-09-10） | [[xl330-cn-bench-kit]] · 原 #1 |

相关：[[microduck-diy]] · [[index]] · [[log]] · [[local-workspace-layout]]
