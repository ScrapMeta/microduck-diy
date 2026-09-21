# Wiki Index

> **Agent 先读：** 本文件 · [[tasks]]（欠什么）· [[log]]（最近 30 条）· [`AGENTS.md`](../AGENTS.md)（规则）
> 本 wiki：`wiki/` · 更新：2026-09-21
> **目标：** 官方原方案完美复刻 · 官方生态完美适配 · 生态内扩展
> **现行焦点（2026-09-19 收拢）：** **整机装配 ＋ 供电链路**（主控/HAT/降压模块/电池 → 母线 **6.0 V**）＋ **官方软件联调**（HAT ＋ 机身 IMU ＋ 1 舵机 · 麦/喇叭）
> （承重项仍在：HAT TTL [#11](https://github.com/ScrapMeta/microduck-diy/issues/11) —— 上总线值 ＋ `0x55` 帧定论）
> 明细见 [[tasks]] 台账（含**最简版本**计划）

## 现行定稿（优先）

### 机身 IMU · imu-to-dxl v0.3

- [[board-imu-to-dxl]] — 总入口（1 号优先 / 2 号暂缓）
- [[imu-to-dxl-firmware-build]] — **固件编译步骤（agent）**
- [[imu-to-dxl-firmware-triage]] — **板级诊断与验收**（`@136` status 位 · 静默零块坑 · 逐块分类 · 2026-09-21）
- [[imu-to-dxl-ref-bom]] — **v0.3 BOM**
- [[imu-to-dxl-ref-schematic]] · [[imu-to-dxl-ref-chip-wiring]] · [[imu-to-dxl-ref-pcb-layout]]
- [[imu-to-dxl-lcsc-order-2026-09-09]] — **v0.3 立创 `SO26090921960`**
- [[imu-to-dxl-lcsc-order-2026-09-05]] — 早期立创订单（对照）

### 装机电控

- [[board-interconnect]] — 装机位置 + DXL 接线（定稿）
- [[body-imu-hat-dxl-power-eval]] — 机身 6 V 经 DXL 回灌 HAT（**不采用** · #9）
- [[elec-three-boards]] — HAT · 机身 IMU · 头（HAT BMI088）
- [[board-hat]] · [[elec-rpi-robot-hat]] — 官方 HAT
- [[hat-solder-kit]] — **HAT 焊接配料 / DNP / 工艺 / 分步测试**
- [[hat-dxl-bus-debug]] — HAT TTL 舵机测不通（**2026-09-16 已打通** · 示波器 + 台供）
- [[dxl-bench-method]] — **台架方法真源**（参数 · 57 600 回退 · `report()` 基线 · M1–M6 · 复测结果）
- [[dual-imu-board-selection]] — 双 IMU 选型结论
- [[elec-three-board-bom]] — 电子 BOM 合并
- [[elec-hat-lcsc-order-2026-09-05]] — HAT 立创订单

### DIY 工程

- [[microduck-diy]] · [[diy-milestones]] · [[diy-bom]]
- [[zero3w-bench-plan]] — **现行：主控台架规划（2G · SD）**
- [[xl330-cn-bench-kit]] — 舵机台架（✅ 通过；**基线已采集**：出厂 ID 1 / 57 600 / shutdown 53）
- `scripts/dxl_ping.py` — **台架 DXL 只读扫/Ping/基线/原始块/同步读脚本**（Protocol 2.0 · 零依赖 · 自带 `self-test`）
- [[local-workspace-layout]] — **布局真源**
- [[ros2-migration-plan]] — ROS2 并行移植规格（software 范畴）
- [[tasks]] — **任务台账**（取代 GitHub Issue · **全员可开 / 更新 / 关**，pm 推送时归档清理）· 规则 [`AGENTS.md`](../AGENTS.md) · 角色手册 `.cursor/skills/`

### 主线执行器 / 采购

- [[xl330-cn-bench-kit]] — 国产启动套件台架（**✅ 通过**；资料后补）
- [[xl330-vs-kpower-rd05t]] — **平替对比（评估中）**：铭牌≈等同 · 接口兼容 · 协议未证 · 台架可判定
- [[rd05t-vendor-inquiry-2026-09-18]] — **问询函**：寄存器兼容 · **P 增益可写性** · 保护阈值（可发送件：同目录 `.pdf`，用 `scripts/md_to_pdf.py` 生成）
- [[xl330-vs-siar-md]] — **平替对比（厂商文档已核 · 2026-09-21）**：寄存器与帧格式**都不是 XL330**（飞特 SCS 血统）· 尺寸/扭矩未给
- [[feetech-hd-1910]] — **飞特 HD-1910 备选执行器**（规格书 A/0；订正脚序 4 处错值）· 协议 [[feetech-scs-bus]] · 已走通路线见 [[microduck-replica]]
- [[robotis]] · [[dynamixel-xl330]] · [[robotis-xl330-order-2026-09-05]]
- [[seeed-bearings]] · [[fastener-bom-study]]
- [[taobao-diy-procurement-2026-09]]

## 官方 Microduck 参考（精简）

- [[microduck]] · [[opensource-coverage]] · [[imu-to-dxl-v2]]（官方契约，未开源板）
- [[pollen-robotics]] · [[hugging-face]] · [[apirrone]] · [[rhoban]]
- [[mechanical-bom-rl]] · [[print-bom-rl]] · [[better-actuator-models-bam]] · [[bam-identification-bench]]
- [[radxa-zero-3w]] · [[radxa]] · [[np-f550-battery]] · [[imx219-camera]] · [[vl53-tof]]
- [[system-flash-armbian]] · [[firmware-flash-matrix]] · [[bench-power-supply]]
- [[microduck-releases]]

## 归档

非现行 Layer-2：[`_archive/`](_archive/README.md)（含 [`_archive/governance/`](_archive/governance/README.md) —— 2026-09-19 停用的旧治理层）。`raw/` 不可变 ingest。

## Raw

清单：[[raw-inventory]]

---

## wiki 规范

> 这一节的规范由 `scripts/wiki_lint.py` **机械执行** —— 脚本的判定即规格。

**领域：** Microduck DIY 复刻知识库（`wiki/`）。

**现行优先级（2026-09-19 收拢）：**

1. **整机装配 ＋ 供电链路** — 主控 / HAT / 降压模块 / 电池叠装，电池 → 降压模块 → HAT 母线 **6.0 V**
2. **官方软件联调** — HAT ＋ 机身 IMU（ID 200）＋ 舵机（ID 1）· 麦 / 喇叭 / 手柄
3. **多板复现 ＋ 装机** — 另 3 块 HAT 焊接测试 · 闲鱼批舵机到货后装 15 台整机
4. **承重项（不阻塞上面）** — HAT TTL `0x55` 帧异常（[#11](https://github.com/ScrapMeta/microduck-diy/issues/11)）· 执行器平替判定（RD05T / 飞特）

官方资料保留为精简参考；非现行调研在 `_archive/`。

**约定**

1. 文件名英文小写 ＋ 连字符（如 `radxa-zero-3w.md`）；正文中文；型号 / 仓库名 / 命令保持原文。
2. **路径从根写**（`wiki/…` · `cad/…`）；参考克隆写 `refs/<clone>/…`；**只引仓名时不加 `refs/`**。
3. 每页 frontmatter：`title` `created` `updated` `type` `tags`（`raw/` 另用 `source_url` · `ingested` · `sha256`）；**改页必须 bump `updated`**。
4. 页间用 wikilink；新页写进本文件对应分节；**新标签先登记下表**；每次动作**追加** [[log]]。
5. **硬规范（frontmatter 字段 · 页长上限 · 死链）由 `scripts/wiki_lint.py` 机械执行 —— 判定即规格**，此处不抄数值。
6. **`raw/` 正文永不改**（纠错写 Layer-2 页）· **不做媒体生产**（`wiki/assets/` 只存原始资料，不生图）。
7. 综合 ≥3 个来源的段落末可加 provenance：`^[raw/articles/….md]`。

**来源与冲突**

- 新来源通常覆盖旧事实（注明日期）；**与本地实测冲突时以本地已克隆仓库 ＋ 实测笔记为准**，并注明对方说法。
- 真冲突**两说并存**（`contradictions:` / `contested: true`），不强行合并。
- **口径差异必须显式标注**：alpha 网格（Pi Zero 2W / np_f970）vs 量产（Radxa / NP-F550）；外形以信息卡 / `*-ref-pcb-layout` 实布为准，MJCF placeholder 尺寸单独标注。

**标签表**（新增标签前必须先登记本表）

| 组 | 标签 |
| --- | --- |
| 组织 | `company` `person` `lab` `open-source` `unitree` |
| 产品 | `product` `pack` `press-kit` `diy` |
| 硬件板 | `board` `hat` `imu` `mcu` `sbc` |
| 执行器传感 | `servo` `dynamixel` `feetech` `tof` `camera` `audio` `nfc` `battery` |
| 供电烧录 | `power` `flash` `emmc` `sd` `firmware` |
| 软件仿真 | `armbian` `runtime` `rl` `sim2real` `bam` `mujoco` |
| 机械 | `mechanical` `bom` `fastener` `assembly` `solder` |
| 工具采购 | `jlceda` `procurement` |
| 元 | `comparison` `query` `index` `workspace` `final` |

**页阈值**

- **建页**：实体 / 概念出现在 2+ 来源，或对单次研究 / 官方文档为中心主题；**不建页**：一笔带过、域外话题。
- **并入已有页**：已有覆盖则更新，不另起同义页。
- **拆分**：超页长上限 → 拆；**例外**（经 Human 批准的「单页件」）记在 `scripts/wiki_lint.py` 的 `OVERSIZE_ACK`（**只减不增**）。
- **归档**：完全被替代 → `_archive/`，并从本 index 移除。

**目录结构**

```
wiki/
├── index.md · tasks.md · log.md
├── raw/         # 不可变 ingest：articles · papers · transcripts · tests · assets
├── assets/      # 原始资料：pcb · procurement · bom（禁止 AI 生图）
├── entities/ · concepts/ · comparisons/ · queries/
├── _archive/    # 被替代页（含 governance/ —— 停用的旧治理层）
└── _meta/       # 索引页（raw-inventory）
```
