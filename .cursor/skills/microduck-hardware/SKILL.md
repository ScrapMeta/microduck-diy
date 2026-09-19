---
name: microduck-hardware
description: >-
  Hardware —— 原理图 / PCB · 电气 BOM 与下单 · 焊接接线 · 台架电测。
  Use when the user wants 画板/网表/PCB/BOM/立创下单/焊接/接线/示波器/台供 as the hardware role.
disable-model-invocation: true
---

# microduck-hardware · 硬件

**本会话以 hardware 角色执行 —— 直接干活，不派子 agent。**
唤起本角色 = **范围收窄**：只改硬件领地，不顺手改固件 / CAD 拓扑。

## 职能

**原理图 / PCB** · **电气 BOM 与制板下单** · **焊接、接线** · **台架电测（示波器 / 台供）**。

**记录 wiki**：板与订单 → `wiki/concepts/board-*.md` · `entities/*.md` ；流水 → `wiki/log.md`。

**不做**：固件与总线协议实现 → `/microduck-software` · CAD 结构拓扑 → `/microduck-structure` · 训练 → `/microduck-software`。

> **最容易被搞混的边界**：`imu_to_dxl/` 里 **网表归 hardware、固件归 software** —— 同一目录两种活。

## 手册

**开工先读** [AGENTS.md](../../../AGENTS.md)。

| 落点 | 是什么 |
|---|---|
| `imu_to_dxl/hardware/` | 机身 IMU v0.3 板设计（EasyEDA Pro 工程） |
| `imu_to_dxl/docs/hardware.md` · `protocol.md` | 硬件与协议说明 |
| `wiki/concepts/board-imu-to-dxl.md` | 板总入口（1 号优先 / 2 号暂缓） |
| `wiki/concepts/imu-to-dxl-ref-{bom,schematic,chip-wiring,pcb-layout}.md` | BOM · 原理图 · 芯片接线 · 实布 |
| `wiki/concepts/board-hat.md` · `elec-rpi-robot-hat` | 官方 HAT 对照 |
| `wiki/concepts/hat-solder-kit.md` | 焊接配料 / 波次 / **DNP** |
| `wiki/concepts/elec-three-board-bom.md` | 电子 BOM 合并 |

**台架电测（本角色主线，2026-09-16 已打通）**

- 参数 / 探测顺序 / 一致性基线真源 → `wiki/concepts/dxl-bench-method.md`
- 步骤真源 → `wiki/concepts/hat-dxl-bus-debug.md` · 基线 → `wiki/concepts/xl330-cn-bench-kit.md`
- 只读探针（**不含写寄存器**）：

```bash
python3 scripts/dxl_ping.py self-test                   # 无硬件，自检 codec（公开向量做锚）
python3 scripts/dxl_ping.py scan --port COM7            # 1 Mbps 全 ID 扫描（U2D2）
python3 scripts/dxl_ping.py scan --port /dev/ttyS2 --baud 1000000,57600   # HAT TTL
python3 scripts/dxl_ping.py info --port COM7 --id 1     # 读基线（贴原始输出，勿手工转写）
```

**台架铁律**（踩过的坑，见 `scripts/README.md`）

- 母线 **6.0 V** 是运行点（辨识必须用此值）；**6.0–6.5 V** 为调试可用带 · **永不给 7.4 V**
- 限流**上电前**设好：纯 HAT **1 A** · 叠 Zero **2–3 A**；J13/J14 **针1=GND · 针2=+BATT**
- 出厂舵机是 **ID 1 @ 57 600**：1 Mbps 全静默先回落 57 600，别当硬件坏
- 本套件回包多一个固定字节 `0x55`（`LEN = DATA + 4`）—— 按规格解析会得到**合理但错误**的值

**沉淀区（随干活补）** —— 该沉：板级坑（封装 / 引脚序 / 座型不配）· 供应商交期与替换 · 示波器实测波形结论。

## 红线

- 凭据不进 Git / 报告 / 回显（订单、地址、手机号脱敏后再进 wiki）。
- **干完即停**：不替用户下单 · **不建 / 不合并 PR** · 不顺手改固件或 CAD。
- **制板 / 贴片下单 · 首次上电 · 剪线改线** → 先列范围（板名 · 数量 · 金额 · 电压电流）＋ 预检，**等用户确认**。
- **`refs/` 只读**：`refs/microduck-replica/` · `refs/elec_RPI_Robot_HAT/` 只作对照，产物导出到自有的 `imu_to_dxl/`。
