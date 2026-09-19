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
> 阶段验收口径仍看 [[diy-milestones]]（含**物料到位表**）；本页只记「当前欠什么」。

## 进行中

| 任务 | 角色 | 验收 | 出处 |
|---|---|---|---|
| **整机装配 ＋ 供电链路**：电池 → 降压模块 → HAT 4P | `/microduck-hardware` | ① 量到 HAT 母线 **6.0 V**（= 运行点，[[bench-power-supply]]）② 记录降压模块型号/额定与实测纹波 ③ **三种模块各过一遍**（5 V/15 A ×1 · 6 V/4 A ×2），说清各自接哪一段 · ④ 叠装顺序（主控/HAT/电池）与固定方式成文 | 2026-09-19 现状收拢 |
| **直供对照**：电池直进 HAT 4P ＋ `Shutdown(63)` 清 bit0（=52）关超压报警 | `/microduck-hardware` | ① 直供 vs 降压两条路径的母线电压/舵机响应对照表 ② 明写这是 **8.4 V > XL330 上限 6.0 V** 的**超规程**验证，**不作装机口径**（[[dynamixel-xl330]]「母线电压天花板」）③ 关保护后的失败模式记清（过压 shutdown 会锁存、须 REBOOT） | 2026-09-19 · [[body-imu-hat-dxl-power-eval]] |
| **HAT TTL：写总线值 ＋ `0x55` 帧异常定论** | `/microduck-hardware` | ① U2D2 ＋ Dynamixel Wizard 交叉验证 `0x55` 来源，**附原始帧**（有 / 无都算结论）② 写 ID / 波特率后在 **1 Mbps** 复验 ③ 示波器：空闲 DATA ≈ 3.3 V · host 包 · 应答包 ④ 限流分级 ＋ 针2 / 5 V / 3V3 实测 | 原 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11) · [[hat-dxl-bus-debug]] · [[dxl-bench-method]] |
| **新焊 3 块 HAT ＋ 分步测试** | `/microduck-hardware` | 每块走 [[hat-solder-kit]] §4（目视 → 短路 → 只 HAT 5 V → 叠 Zero → i2c `0x18` → 喇叭/麦 → DXL 单舵机）；**顺带勾掉该页两处旧欠项**（i2c `0x18` 明细 · J1 喇叭出声） | 2026-09-19 现状收拢 |
| **官方软件部署联调**：HAT ＋ 机身 IMU ＋ 1 舵机 | `/microduck-software` | 官方 daemon 起得来 · 总线上**同时**认到 **ID 200**（机身 IMU）与 **ID 1**（XL330）· 麦克录到一段 · J1 喇叭出声 · 失败留 dmesg ＋ 退出码 | v0.1 未勾项 · [[diy-milestones]] |
| **机身 IMU 改竖装 `power_support` 背板** | `/microduck-structure` | 竖装不干涉电池 / 腿 / 线束 · 孔位与所需线长写回 [[mechanical-bom-rl]] · [[board-interconnect]] §1 | 2026-09-19 现状收拢 |

## 待办

| 任务 | 角色 | 验收 | 出处 |
|---|---|---|---|
| **闲鱼舵机到货清点 ＋ 装机**（5 国产组装 ＋ 9 原厂 = **14**） | `/microduck-hardware` | 逐台 `scripts/dxl_ping.py info` 采基线（ID/波特率/固件/电压，格式照 [[xl330-cn-bench-kit]] 表）· **国产组装件 vs 原厂件**寄存器差异进 [[dynamixel-xl330]] · 到货 **14 ＋ 现有 1 = 15 台**，按 [[board-interconnect]] ID 图配置装机 | 2026-09-19 |
| **手柄冒烟**：Xbox（在手）· 亚博智能 PS2（待试） | `/microduck-software` | 与官方 `refs/microduck/configd/src/pad.rs` 按键表**逐键对齐**；配不配得上写清；结论落新页 | 2026-09-19 |
| **喇叭 / ToF 到货后先测** | `/microduck-software` | 喇叭 **3525 · 4 Ω 3 W** 接 **J1**（[[hat-solder-kit]] §4.6），**先用旧喇叭打样**；VL53**L8CX** 到货后按 [[vl53-tof]] 试 `0x29` / `0x52` 两地址，**买的是 L8CX 要记明**（在役多数为 L5CX） | 2026-09-19 |
| **本轮物料事实落页**（料号 / 订单 / 实物尺寸） | `/microduck-hardware` | 降压模块 ×3 · 闲鱼批 · ToF · 喇叭 · 摄像头 ×2 · 电池 ×2＋双充 → [[diy-bom]] §C/§E · [[np-f550-battery]] · [[imx219-camera]] · [[vl53-tof]] | 2026-09-19 |
| 拆页：3 页超 200 行上限 | `/microduck-pm` 收口 · 内容归 `/microduck-hardware` | `hat-solder-kit` **399** → 3 页（配料/DNP · 焊接工艺 · 分步测试）· `xl330-vs-kpower-rd05t` **220** → 2 页（事实层 · 判断层）· `rd05t-vendor-inquiry` **203**（对外可发送件 —— 拆前先定「单页件是否该有例外」）。**只减不增**：记账表在 `scripts/wiki_lint.py` 的 `OVERSIZE_ACK`，拆完从表里删掉 | 治理改造 2026-09-19 |
| replica0908 焊接 ＋ U2D2 冒烟（对照 #7 零回包） | `/microduck-hardware` | MCU＋PHY＋电源＋DXL 座＋SWD 可贴完 · CubeProgrammer 能下载 · Ping / Read 结果写清「有回包 / 仍零回包」· 与 #7 对照一句话 | 原 [#8](https://github.com/ScrapMeta/microduck-diy/issues/8) · [[microduck-replica]] |
| 结构可干装配 | `/microduck-structure` | 打印件 / 紧固件 / 轴承 / XL330 装得上 · 件数进 [[mechanical-bom-rl]] | v0.1 未勾项 |
| 契约对齐：DXL / IMU / 策略接口与官方生态一致 | `/microduck-software` | [[opensource-coverage]] 无未决缺口 | v0.1 未勾项 |
| RD05T 问询函发出 ＋ 回函落 wiki | `/microduck-hardware` | [[rd05t-vendor-inquiry-2026-09-18]] 已出 PDF（同目录）· 回函结论进 [[xl330-vs-kpower-rd05t]] | log 2026-09-18 |
| 回收上游 `microduck-replica` 那 9 个提交 | `/microduck-software` ／ `/microduck-hardware` | 飞特官方内存表升为**厂商一手**（订正 [[xl330-vs-feetech-servos]]）· 网页舵机调试台 · imu_to_dxl 首板 PH 座实测（J4/J5） | log 2026-09-19 |
| 喇叭出声孔 · ToF breakout 外形：实测 | `/microduck-structure` | 实测值写回 [[hat-solder-kit]] §6.3 · [[vl53-tof]]（当前均标「查不出，不猜」；ToF 到货后即可量） | log 2026-09-19 |

## 已完成（近 30 天）

| 任务 | 结论 | 落点 |
|---|---|---|
| 机身 IMU v0.3 固件 P0 修复 ＋ U2D2 验收 | Ping/Read 1000 · SyncRead 10 min 无超时（`a49a628`） | [[imu-to-dxl-firmware-build]] · 原 #10 |
| 机身 6 V 经 DXL 回灌 HAT 评估 | **不采用** —— 电池经降压模块稳在 6.0 V 长期运行 | [[body-imu-hat-dxl-power-eval]] · 原 #9 |
| HAT TTL 舵机 bring-up | **已打通**：出厂 ID 1 @ 57 600 应答复现 · 基线已采集 | [[hat-dxl-bus-debug]] · [[xl330-cn-bench-kit]] · 原 #4 |
| Zero 3W P1 相机台架 | probe `0x0219` · `/dev/video0` 可抓 NV12 · **两颗模块（Pi Cam V2 ＋ 亚博 IMX219）均过** | [[imx219-camera]] · [[zero3w-bench-plan]] · 原 #5 |
| HAT 配料焊接 | 首板完成（DNP 项已省）· 另备 **3 块待焊**（见「进行中」） | [[hat-solder-kit]] · 原 #3 |
| 机身 IMU 板：焊接 **5** 块 · 烧录 **3** 块 | 尚缺逐板基线与装机分配 | [[board-imu-to-dxl]] · [[imu-to-dxl-firmware-build]] |
| Zero 3W P0 系统台架 | flash / boot / SSH 通过 | [[zero3w-bench-plan]] · 原 #2 |
| XL330-CN 舵机台架冒烟 | 通过（2026-09-10） | [[xl330-cn-bench-kit]] · 原 #1 |
| 物料：电池 ＋ 降压模块 到货 | F550 **×2** ＋ 双充（2 位）· 降压模块 **5 V/15 A ×1 · 6 V/4 A ×2** | [[np-f550-battery]] · [[bench-power-supply]] |
| 物料：舵机两批下单 | **原厂单** [[robotis-xl330-order-2026-09-05]]（延误，预计 **10 月中旬**可能发）· **闲鱼批** 5 国产组装 ＋ 9 原厂（预计 **09-21 周一**到） | [[diy-bom]] §C |
| 物料：在途 | VL53**L8CX** ToF · 喇叭 **3525 4 Ω 3 W** —— 均预计 **09-23 周三**到 | [[vl53-tof]] · [[hat-solder-kit]] §6.3 |

相关：[[microduck-diy]] · [[index]] · [[log]] · [[diy-milestones]] · [[local-workspace-layout]]
