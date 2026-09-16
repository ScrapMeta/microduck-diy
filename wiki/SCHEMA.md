# Wiki Schema（llm-wiki · Microduck DIY）

> **Agent 每次会话必须先读：** 本文件 → [`index.md`](index.md) → [`log.md`](log.md)（最近 30 条）

## Domain

**Microduck DIY 复刻知识库**（`microduck-diy/wiki`）。

**项目目标：** 官方原方案完美复刻 · 官方生态完美适配 · 生态内扩展硬件与玩法。

**现行工作优先级：**

1. **机身 IMU `imu-to-dxl v0.3`**（1 号 32×22）— 原理图 / PCB / BOM / 互联  
2. **装机电控定稿** — HAT + 总线 + 互联  
3. **DIY BOM / 里程碑** — 与上两项对齐的采购与进度  

官方资料保留为精简参考。非现行调研在 **`_archive/`**。

工作区根：`D:\projects\microduck` · 本 wiki：`D:\projects\microduck\microduck-diy\wiki`。  
diy 仓：`imu_to_dxl/` · `wiki/` · `cad/`。治理：`docs/agent-governance.md`（**v0.8：GitHub 基础工程 + llm-wiki；只常驻 pm；无 handoff**）；入口 `AGENTS.md`。`microduck_ros2` **不在本 wiki 主轴**（并入 software 范畴）。

## Conventions

- 文件名：英文小写 + 连字符（如 `radxa-zero-3w.md`）
- 正文：中文为主；型号、仓库名、命令保持原文
- 每页 YAML frontmatter（见下）
- 使用 `[[wikilinks]]` 互链；**每页 ≥2 出站 wikilink**
- 更新页面必须 bump `updated`
- 新页必须写入 `index.md` 对应分节
- 每次动作必须 **追加** `log.md`
- 页长 ≤ **200 行**；超长拆分子页
- 综合 ≥3 个来源的段落末可加 provenance：`^[raw/articles/....md]`
- **禁止修改 `raw/` 正文**（仅允许新建 ingest；纠错写在 Layer-2 页；`sha256` 等 frontmatter 元数据可补全）
- **不做媒体生产**：本仓不生图、不合成小红书封面、不跑 baoyu/生图流水线；`wiki/assets/` 只保存 CAD/官方/采购等**原始资料**截图与文件

## Frontmatter（Layer-2）

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: []
sources: []
confidence: high | medium | low
related: []
---
```

## raw/ Frontmatter

```yaml
---
source_url: https://...   # 或 null
ingested: YYYY-MM-DD
sha256: <body hex digest>
---
```

## Tag Taxonomy

新增标签前必须先写入本表。

| 组 | 标签 |
| --- | --- |
| 组织 | `company` `person` `lab` `open-source` `unitree` |
| 产品 | `product` `pack` `press-kit` `diy` |
| 硬件板 | `board` `hat` `imu` `mcu` `sbc` |
| 执行器传感 | `servo` `dynamixel` `feetech` `tof` `camera` `audio` `nfc` `battery` |
| 供电烧录 | `power` `flash` `emmc` `sd` `firmware` |
| 软件仿真 | `armbian` `runtime` `rl` `sim2real` `bam` `mujoco` |
| 机械 | `mechanical` `bom` `fastener` |
| 工具采购 | `jlceda` `procurement` |
| 元 | `comparison` `query` `index` `workspace` `final` |

## Page Thresholds

- **建页**：实体/概念出现在 2+ 来源，或对单次研究/官方文档为中心主题
- **并入已有页**：已有覆盖则更新，不另起同义页
- **不建页**：一笔带过、域外话题
- **拆分**：>200 行
- **归档**：完全被替代 → `_archive/`，并从 index 移除

## 目录结构

```
wiki/
├── SCHEMA.md · index.md · log.md
├── raw/
│   ├── articles/      # 官方/外部文档摘录
│   ├── papers/
│   ├── transcripts/   # 研究会话整理（immutable）
│   ├── tests/
│   └── assets/
├── assets/            # CAD/官方截图、采购 XLS、BOM CSV（禁止 AI 生图）
│   ├── pcb/
│   ├── procurement/
│   └── bom/
├── entities/
├── concepts/
├── comparisons/
├── queries/
├── _archive/          # 被替代页
└── _meta/
```

## Update Policy

1. 新来源通常覆盖旧事实；注明日期
2. 真冲突：两说并存 + `contradictions:` / `contested: true`
3. Press Kit / 官方文档 vs 本地仓库：以**本地已克隆仓库 + 实测笔记**为准写 Layer-2，并注明 Press Kit 说法
4. alpha 网格（Pi Zero 2W / np_f970）与量产（Radxa / NP-F550）差异必须显式标注
5. **外形口径**：DIY 板框以信息卡 / `*-ref-pcb-layout` 实布为准；MJCF placeholder 尺寸单独标注，勿与实布混写

## Agent 第一站

1. 本 SCHEMA → index（**现行定稿**）→ 最近 log  
2. 问机身 IMU / v0.3 BOM·原理图·PCB → [[board-imu-to-dxl]] · [[imu-to-dxl-ref-bom]] · [[imu-to-dxl-ref-schematic]] · [[imu-to-dxl-ref-pcb-layout]]  
3. 问装机接线 / 三板 → [[board-interconnect]] · [[elec-three-boards]] · [[board-hat]]  
4. 问 DIY 进度 / BOM → [[microduck-diy]] · [[diy-milestones]] · [[diy-bom]]  
5. 问官方契约 / 开源缺口 → [[opensource-coverage]] · [[imu-to-dxl-v2]] · 固件 `../imu_to_dxl/`  
6. 问 XL330 / 采购 → [[dynamixel-xl330]] · [[robotis-xl330-order-2026-09-05]]  
7. 问烧录/供电 → [[system-flash-armbian]] · [[bench-power-supply]] · [[firmware-flash-matrix]]  
8. 问工作区 → [[local-workspace-layout]]  
9. 非现行页 → `_archive/`
