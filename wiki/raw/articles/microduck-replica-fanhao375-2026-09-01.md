---
source_url: https://github.com/fanhao375/microduck-replica
ingested: 2026-09-01
sha256: 7b9ff1280fdfeaf2baadff6f7fb1a9bdc44c2a4ad6647edf302efe26b0383735
note: 第三方复刻仓库书签；未并入 Layer-2 实体/概念正文
---

# Microduck Replica（fanhao375）来源记录

> **用途**：单独登记外部仓库链接与目录要点。  
> **边界**：本文件为 raw ingest / 书签；**不要**把其中结论直接合并进 `entities/` `concepts/` 等主 wiki 页，除非另开一次显式 ingest→lint 流程。

## 链接

- Repo: https://github.com/fanhao375/microduck-replica
- Default branch: `master`
- 简述（仓库自述）：从官方 MJCF / Rust 源码反推装配图、CAD 装配体与电控方案的第三方复刻研究
- 许可证（仓库自述）：`scripts/` Apache-2.0；`assembly-drawings/` `cad/` 依上游 CC BY-SA-NC

## 顶层目录（2026-09-01 抓取）

| 路径 | 内容概要 |
|------|----------|
| `README.md` / `README.en.md` | 总览、装配树、可行性与复刻路径 |
| `PROGRESS.md` | 批次进度与决策记录 |
| `assembly-drawings/` | 7 张装配/爆炸/分色图（PNG） |
| `cad/` | 已应用世界变换的 STL（整机 + 15 部件）+ `零件对照表.json` |
| `docs/` | 硬件逆向、规格速查、紧固件、执行器、社区动态 |
| `scripts/` | 拉上游、渲染装配图、导出 CAD、扫孔 |
| `tools/stl_viewer.html` | STL 查看器 |

## docs/ 文件名清单

- `硬件方案逆向.md`
- `硬件规格速查.md`
- `紧固件反推.md`
- `执行器选型.md`
- `社区动态.md`
- `hole_analysis.json`

## 仓库自述中的复刻优先级（摘录，非本库结论）

- 优先自画：`imu_to_dxl`（LSM6DSV16X + MCU + 半双工 TTL；DXL 从机）
- HAT 可简化或省略（不要音频时）
- 主控自称与官方同为市售 Radxa Zero 3W
- 仿真 STL ≠ 可打印工程件；走线方案缺失

## 抓取说明

- 抓取方式：`gh api` 列目录 + 拉取 README / 部分 docs 原文
- 未将本仓库 clone 进 `D:\projects\microduck`
- 未改写本 workspace 主 wiki 的 entity/concept 页
