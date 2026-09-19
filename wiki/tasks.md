---
title: 任务台账
created: 2026-09-19
updated: 2026-09-19
type: index
tags: [index, workspace]
---

# 任务台账

> **取代 GitHub Issue** —— 历史 Issue #1–#11 与 Milestone `v0.1` 已冻结只读（见 [AGENTS.md](../AGENTS.md)「GitHub」）。
> 一行 = 一件事。收工在 [`log.md`](log.md) 追加一条；**完成 / 关闭的整行搬到 [`tasks-done.md`](tasks-done.md)**。
> 阶段验收口径仍看 [[diy-milestones]]（含**物料到位表**）；本页只记「当前欠什么」。

**编号** —— `T-01` 起，**一经分配不再变动、不复用**；任务完成后**编号随行**搬进 `tasks-done.md`。
用途：让 `log.md`、页间引用和对话都能指认同一条任务，不用抄任务名。
编号自 2026-09-19 启用；此前的条目见 [`tasks-done.md`](tasks-done.md)（无编号，靠 `出处` 追溯）。

**「阻塞源」决定顺序，不是优先级。** 未标 = 可在手推进。

| 记号 | 含义 | 怎么解 |
|---|---|---|
| 🖐 | **台架** —— 要你本人坐到台架前 ＋ 上电（红线 6：只有你能签） | 多个 🖐 之间是**串行**，不是并行；排顺序 ≠ 能同时推 |
| 🟢 | **agent 可独立推** —— 不占台架、不需上电 | 你不坐台架时也能走 |
| ⏳ | **等外部到货** —— 有日期，现在动不了 | 到货日回到「待办」 |
| ✋ | **等你本人动作** —— 不是技术阻塞 | 你点头 / 出门一趟 |
| ⚠️ | **待你确认才能定** —— 台账缺事实 | 你补一句就行 |

**两条上限**（防台账自己长胖）：

- **进行中 ≤ 3** —— 一个人 ＋ 一个台架推不了更多；多认领只会让「进行中」变成自我欺骗。
- **活跃 ≤ 12**（进行中 ＋ 待办 ＋ 等外部）—— **满了要开新的，就先关掉一条**。
- **无界验收**（开口、永远勾不掉）必须先收窄才准立项。

## 进行中（3/3）

| 编号 | 任务 | 阻塞 | 角色 | 验收 | 出处 |
|---|---|---|---|---|---|
| **T-01** | **整机装配 ＋ 供电链路**：电池 → 降压模块 → HAT 4P | 🖐 台架 | `/microduck-hardware` | ① 量到 HAT 母线 **6.0 V**（= 运行点，[[bench-power-supply]]）② 记录降压模块**型号/额定 ＋ 实测纹波**（三种各一遍：5 V/15 A ×1 · 6 V/4 A ×2，说清各自接哪一段）③ **叠装顺序**（主控 / HAT / 电池）与固定方式成文 | 2026-09-19 现状收拢 · [[index]] 优先级 ① |
| **T-02** | **官方软件部署联调**：HAT ＋ 机身 IMU ＋ 1 舵机 | 🖐 台架 | `/microduck-software` | 官方 daemon 起得来 · 总线上**同时**认到 **ID 200**（机身 IMU）与 **ID 1**（XL330）· 麦克录到一段 · J1 喇叭出声 · 失败留 dmesg ＋ 退出码 | v0.1 未勾项 · [[index]] 优先级 ② |
| **T-03** | **新焊 3 块 HAT ＋ 分步测试** | 🖐 台架（**焊接不占**） | `/microduck-hardware` | 每块走 [[hat-solder-kit]] §4（目视 → 短路 → 只 HAT 5 V → 叠 Zero → i2c `0x18` → 喇叭/麦 → DXL 单舵机）；**顺带勾掉该页两处旧欠项**（i2c `0x18` 明细 · J1 喇叭出声）。板料件齐，**焊接可在台架等待间隙做** | 2026-09-19 现状收拢 · [[index]] 优先级 ③ |

## 待办

| 编号 | 任务 | 阻塞 | 角色 | 验收 | 出处 |
|---|---|---|---|---|---|
| **T-04** | **HAT TTL：写总线值 ＋ `0x55` 帧异常定论** | 🖐 台架 | `/microduck-hardware` | ① U2D2 ＋ Dynamixel Wizard 交叉验证 `0x55` 来源，**附原始帧**（有 / 无都算结论）② 写 ID / 波特率后在 **1 Mbps** 复验 ③ 示波器：空闲 DATA ≈ 3.3 V · host 包 · 应答包 ④ 限流分级 ＋ 针2 / 5 V / 3V3 实测 | 原 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11) · [[hat-dxl-bus-debug]] · [[dxl-bench-method]] |
| **T-05** | **直供对照**：电池直进 HAT 4P ＋ `Shutdown(63)` 清 bit0（=52）关超压报警 | 🖐 台架 | `/microduck-hardware` | ① 直供 vs 降压两条路径的母线电压 / 舵机响应对照表 ② 明写这是 **8.4 V > XL330 上限 6.0 V** 的**超规程**验证，**不作装机口径**（[[dynamixel-xl330]]「母线电压天花板」）③ 关保护后的失败模式记清（过压 shutdown 会锁存、须 REBOOT） | 2026-09-19 · [[body-imu-hat-dxl-power-eval]] |
| **T-06** | 机身 IMU 改竖装 `power_support` 背板 | 🟢 | `/microduck-structure` | 竖装不干涉电池 / 腿 / 线束 · 孔位与所需线长写回 [[mechanical-bom-rl]] · [[board-interconnect]] §1 | 2026-09-19 现状收拢 |
| **T-07** | 手柄冒烟：Xbox（在手）· 亚博智能 PS2（待试） | 🟢 | `/microduck-software` | 与官方 `refs/microduck/configd/src/pad.rs` 按键表**逐键对齐**；配不配得上写清；结论落新页 | 2026-09-19 |
| **T-08** | 拆页：3 页超 200 行上限 | 🟢 | `/microduck-pm` 收口 · 内容归 `/microduck-hardware` | `hat-solder-kit` **399** → 3 页（配料/DNP · 焊接工艺 · 分步测试）· `xl330-vs-kpower-rd05t` **220** → 2 页（事实层 · 判断层）· `rd05t-vendor-inquiry` **203**（对外可发送件 —— 拆前先定「单页件是否该有例外」）。**只减不增**：拆完从 `scripts/wiki_lint.py` 的 `OVERSIZE_ACK` 删条目 | 治理改造 2026-09-19 |
| **T-09** | 宿主工具链清理（Windows 开发机 · 系统级） | ✋ 等你逐项点头 | `/microduck-pm` | ① 删 `C:\Python\Python38`（**1648 MB**，已无 `python.exe`）＋ 从**机器 PATH** 移除其两条路径（机器 PATH 排在用户 PATH 之前，坏 exe 抢 `tensorboard` / `huggingface-cli` / `modelscope`）② 删 `C:\Python\Python39`（92 MB）＋ 清 HKLM `PythonCore\3.9` ③ `C:\Python\miniconda3`（**871 MB**）留删**待定** ④ 关商店 `python3.exe` 执行别名（GUI，人操作）。**均属破坏性 / 系统级** | 2026-09-19 · [[local-workspace-layout]] §宿主工具链 |
| **T-10** | RD05T 问询函发出 ＋ 回函落 wiki | ✋ 等你寄 | `/microduck-hardware` | [[rd05t-vendor-inquiry-2026-09-18]] 已出 PDF（同目录）· 回函结论进 [[xl330-vs-kpower-rd05t]] | log 2026-09-18 |

## 等外部（挂起 · 到货日回「待办」）

| 编号 | 任务 | 阻塞 | 角色 | 验收 | 出处 |
|---|---|---|---|---|---|
| **T-11** | **闲鱼舵机到货清点 ＋ 装机**（5 国产组装 ＋ 9 原厂 = **14**） | ⏳ **09-21 周一** | `/microduck-hardware` | 逐台 `scripts/dxl_ping.py info` 采基线（ID/波特率/固件/电压，格式照 [[xl330-cn-bench-kit]] 表）· **国产组装件 vs 原厂件**寄存器差异进 [[dynamixel-xl330]] · 到货 **14 ＋ 现有 1 = 15 台**，按 [[board-interconnect]] ID 图配置装机 · **料号落 [[diy-bom]] §C** | 2026-09-19 |
| **T-12** | **ToF / 喇叭到货：功能 ＋ 外形实测** | ⏳ **09-23 周三** | `/microduck-software` ＋ `/microduck-structure` | ① 喇叭 **3525 · 4 Ω 3 W** 接 **J1**（[[hat-solder-kit]] §4.6），**先用旧喇叭打样** ② VL53**L8CX** 按 [[vl53-tof]] 试 `0x29` / `0x52` 两地址，**买的是 L8CX 要记明**（在役多数为 L5CX）③ 外形实测（**喇叭出声孔 · ToF breakout**）写回 [[hat-solder-kit]] §6.3 · [[vl53-tof]]（当前均标「查不出，不猜」）④ 料号进 [[diy-bom]] §E | 2026-09-19 |

> **合并说明**：原「喇叭 / ToF 到货后先测」＋「喇叭出声孔 · ToF breakout 外形实测」两行合并 ——
> 同一到货日、只要能到就同时能做，拆成两行只是让台账看起来更长。
> **删除说明**：原「本轮物料事实落页」整行删掉 —— 它没有自己的触发条件，是各宿主任务的**收尾动作**，
> 验收已分发：降压模块 → T-01；闲鱼批 → T-11；ToF/喇叭 → T-12；摄像头/电池已在手且已有页。

**已完成 / 已关闭** → [`tasks-done.md`](tasks-done.md)（只追加，不删）。本页不再保留历史行。

相关：[[microduck-diy]] · [[index]] · [[log]] · [[tasks-done]] · [[diy-milestones]] · [[local-workspace-layout]]
