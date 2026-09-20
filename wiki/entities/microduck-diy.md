---
title: microduck-diy
created: 2026-09-01
updated: 2026-09-20
type: entity
tags: [diy, workspace, open-source, mechanical]
sources: []
confidence: high
related:
  - diy-milestones
  - diy-bom
  - local-workspace-layout
  - board-imu-to-dxl
  - opensource-coverage
---

# microduck-diy（手搓小小鸭）

个人 DIY 工程仓，面向官方 [[microduck]]。

| 字段 | 值 |
|------|-----|
| GitHub | `https://github.com/ScrapMeta/microduck-diy` |
| 本地 | `D:\projects\microduck\microduck-diy` |
| 小红书 | **精钢葫芦娃** |
| 公众号 | **人工具身智能** |
| **当前版本计划** | **最简版本**（见 [[tasks]]） |

## 目标

1. **完美复刻**官方原方案  
2. **完美适配**官方生态（HAT、Dynamixel 总线、策略/运行时契约）  
3. 在官方生态下**扩展**硬件与玩法（不另起平行协议栈）

## 仓内结构

| 路径 | 角色 |
|------|------|
| `imu_to_dxl/` | 机身 IMU **v0.3** 硬件 + 参考固件 |
| `wiki/` | 本知识库 |
| `cad/` | 耐久 **`.3mf`** |
| `README.md` | 工程说明 |

相关：[[diy-milestones]] · [[diy-bom]] · [[board-imu-to-dxl]] · [[local-workspace-layout]]
