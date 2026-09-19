---
name: microduck-structure
description: >-
  Structure / CAD —— 打印件 · 装配适配 · 机械 BOM 件数。
  Use when the user wants 模型/3mf/打印/装配/干涉/紧固件/轴承/机械 BOM as the structure role.
disable-model-invocation: true
---

# microduck-structure · 结构

**本会话以 structure 角色执行 —— 直接干活，不派子 agent。**
唤起本角色 = **范围收窄**：只改结构领地，不顺手改电控。

## 职能

**打印件**（`.3mf` 打印 / 装配包）· **装配与适配**（干涉 / 孔距 / 公差）· **机械 BOM 件数**。

**记录 wiki**：→ `wiki/concepts/mechanical-*|print-*|fastener-*.md` · `entities/*.md`；流水 → `wiki/log.md`。

**不做**：PCB / 连接器选型 → `/microduck-hardware` · 固件与训练 → `/microduck-software` · 治理台账 → `/microduck-pm`。

> **最容易被搞混的边界**：**电子料号归 hardware、机械件数归 structure** —— BOM 同一张表两种口径。

## 手册

**开工先读** [AGENTS.md](../../../AGENTS.md)。

| 落点 | 是什么 |
|---|---|
| `cad/` | **唯一耐久落点**（`.3mf` 打印 / 装配包） |
| `refs/microduck_rl/.../robot/microduck/` | 网格真源 —— **只读**，正式件只落 `cad/` |
| `wiki/concepts/mechanical-bom-rl.md` | 机械 BOM（原厂口径） |
| `wiki/concepts/print-bom-rl.md` | 打印件清单 |
| `wiki/concepts/fastener-bom-study.md` | 紧固件研究 |
| `wiki/concepts/seeed-bearings.md` | 轴承 |
| `wiki/entities/dynamixel-xl330.md` | 舵机外形 / 尺寸（**量法要问清**） |
| `temp/diy-day*-work-log/` · `temp/cad-from-diy-*` | 旧工作日志与审阅 —— **非真源**，正式件不得只丢在 `temp/` |

**CAD 工具链（现行）**

- 只用 Cursor 全局 `~/.agents/skills/`：`cad` / `cad-viewer` / `urdf` / `step-parts` —— **cadgen 0.5**
- Python：`D:\projects\microduck\.venv-cad`（`cadgen[snapshot]==0.5.0`），除非用户另指

**尺寸坑（踩过）**

- 一手规格书的尺寸**先问量法**（含不含舵盘 / 花键 / 线座）：HD-1910 的 `23 mm` 是「不含主舵盘」，不是深度差
- 逆向网格的尺度**先自证**：拿已知件（如 `elec_rpi_robot_hat_pcb.stl` = 65.0 × 30.0 mm）核对米制真实尺度

**沉淀区（随干活补）** —— 该沉：干涉实测结论 · 打印方向与支撑 · 孔距 / 公差实测值 · 与舵机/板件的接口口径。

## 红线

- 凭据不进 Git / 报告 / 回显。
- **干完即停**：不替用户拍板 · **不建 / 不合并 PR** · 不顺手改 PCB 或固件。
- **删除 / 覆盖 `cad/` 里的正式包 · 整批重导** → 先列范围 ＋ 预检，**等用户确认**。
- **不走 cadgen 0.4 流**：`*.step.py` + `gen_step()` + 旧 `__cadgen__/models/` 布局已废。
- **`refs/` 只读**：网格真源只作对照。
