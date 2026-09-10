---
source_url: https://github.com/JoyandAI/OpenMicroDuck
ingested: 2026-09-08
sha256: pending
note: 刷新 ingest；本地已 clone；舵机 HD-1910 / HL-2909 已建 Layer-2
---

# OpenMicroDuck（JoyandAI）来源记录

> raw ingest。Layer-2：[[openmicroduck]] · [[feetech-hd-1910]] · [[feetech-hl-2909]]。

## 链接与本地

- Repo: https://github.com/JoyandAI/OpenMicroDuck
- 本地：`D:\projects\microduck\OpenMicroDuck`（shallow clone · HEAD `2c54375` · 2026-09-06）
- Stars：约 56（API 2026-09-08）

## 仓库现状（相对 2026-09-04 书签）

已有：`docs/`（servo、architecture、main_controller 等）、`hardware_spec/servo/`（HD-1910 外形图、HL-2915/2909 规格书、ED330 图）、`cad/`（含 HD-1910 STEP）、样机照片、中英 README。

## 舵机要点（摘自 docs/servo.md）

| 型号 | 电压 | 备注 |
|------|------|------|
| HD-1910M/C001 | 5–8.4 V | 开源小鸭预售款；堵转 10 kg·cm；额定 3.0 |
| HL-2909-C001 | 9–14 V | 样机所用；规格书与 HL-2915-C002 同册 |
| ED330 | 5–8.4 V | 额定负载口径与 HD-1910 冲突，勿混用 |
| Unitree S288 | ~12.6 V | 外形最贴 XL330；协议/ID 范围另议 |

换舵机须重训策略。细节以仓内 PDF/产品页为准。
