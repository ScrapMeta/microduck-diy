---
title: 已完成任务
created: 2026-09-19
updated: 2026-09-19
type: index
tags: [index, workspace]
---

# 已完成任务

> 本页是 [`tasks.md`](tasks.md) 的**已完成 / 已关闭分区** —— 拆出来只为让活动台账保持可读。
> **只追加，不删**：行一旦落到本页就不再改动（原行永远在 git 历史里）。
> 编号自 2026-09-19 启用 —— 之后完成的条目**带编号搬过来**；此前的条目**无编号**，靠 `出处` 与 [`log.md`](log.md) 追溯。

## 已完成（近 30 天）

| 编号 | 任务 | 结论 | 落点 |
|---|---|---|---|
| — | 结构可干装配 | **已完成**（2026-09-19 Human 确认「打印件 / 紧固件 / 轴承 11＋3 / XL330 均装得上」）。⚠️ `件数是否已并入` [[mechanical-bom-rl]] **未核实**；[[diy-milestones]] 对应行**未改勾**（同行含未完成的机身 IMU 竖装 → **T-06**） | [[mechanical-bom-rl]] |
| — | 机身 IMU v0.3 固件 P0 修复 ＋ U2D2 验收 | Ping/Read 1000 · SyncRead 10 min 无超时（`a49a628`） | [[imu-to-dxl-firmware-build]] · 原 #10 |
| — | 机身 6 V 经 DXL 回灌 HAT 评估 | **不采用** —— 电池经降压模块稳在 6.0 V 长期运行 | [[body-imu-hat-dxl-power-eval]] · 原 #9 |
| — | HAT TTL 舵机 bring-up | **已打通**：出厂 ID 1 @ 57 600 应答复现 · 基线已采集 | [[hat-dxl-bus-debug]] · [[xl330-cn-bench-kit]] · 原 #4 |
| — | Zero 3W P1 相机台架 | probe `0x0219` · `/dev/video0` 可抓 NV12 · **两颗模块（Pi Cam V2 ＋ 亚博 IMX219）均过** | [[imx219-camera]] · [[zero3w-bench-plan]] · 原 #5 |
| — | HAT 配料焊接 | 首板完成（DNP 项已省）· 另备 **3 块待焊**（→ **T-03**） | [[hat-solder-kit]] · 原 #3 |
| — | 机身 IMU 板：焊接 **5** 块 · 烧录 **3** 块 | 尚缺逐板基线与装机分配 | [[board-imu-to-dxl]] · [[imu-to-dxl-firmware-build]] |
| — | Zero 3W P0 系统台架 | flash / boot / SSH 通过 | [[zero3w-bench-plan]] · 原 #2 |
| — | XL330-CN 舵机台架冒烟 | 通过（2026-09-10） | [[xl330-cn-bench-kit]] · 原 #1 |
| — | 物料：电池 ＋ 降压模块 到货 | F550 **×2** ＋ 双充（2 位）· 降压模块 **5 V/15 A ×1 · 6 V/4 A ×2** | [[np-f550-battery]] · [[bench-power-supply]] |
| — | 物料：舵机两批下单 | **原厂单** [[robotis-xl330-order-2026-09-05]]（延误，预计 **10 月中旬**可能发）· **闲鱼批** 5 国产组装 ＋ 9 原厂（预计 **09-21 周一**到） | [[diy-bom]] §C |

## 已关闭（未完成 · 不再追）

| 编号 | 任务 | 关闭理由 | 日期 |
|---|---|---|---|
| — | *（暂无）* | 关闭 = 明确不追，理由必须写清；**不是淡出** —— 淡出的留在 `tasks.md` 的「等外部」 | — |

> **关闭 ≠ 完成**：完成要过 `tasks.md` 里写明的验收；关闭是判定「不值得再做 / 已被别的任务吸收」。
> 两者都搬进本页，但落**不同表**，免得后人把「没做」读成「做完了」。

相关：[[tasks]] · [[index]] · [[log]] · [[diy-milestones]] · [[microduck-diy]]
