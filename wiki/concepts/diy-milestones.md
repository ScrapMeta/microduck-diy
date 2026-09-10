---
title: DIY 里程碑
created: 2026-09-03
updated: 2026-09-10
type: concept
tags: [diy, workspace, open-source]
sources: []
confidence: medium
related:
  - microduck-diy
  - diy-bom
  - board-interconnect
  - dual-imu-board-selection
  - imu-to-dxl-v2
  - elec-rpi-robot-hat
  - opensource-coverage
---

# DIY 里程碑

[[microduck-diy]] 的项目阶段用语义化版本号（`v0.x`）标记。

## 项目目标

1. **完美复刻**官方 [[microduck]] 原方案  
2. **完美适配**官方生态（可对接官方软件栈与总线契约）  
3. 在官方生态下**扩展**硬件与玩法  

v0.1 阶段验收口径（可联调）：主控 + 舵机总线 + 机身 IMU + 供电，并能部署官方行走相关策略。

## 里程碑表

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| **v0.1** | **当前** | 官方方案可复现联调（进行中） |
| v0.2+ | 未开 | v0.1 验收后再定 |

### v0.1 验收（草稿）

- [ ] 机械：结构可干装配（打印 / 紧固件 / 轴承 / [[dynamixel-xl330]]）
- [ ] 电控：[[radxa-zero-3w]] + [[elec-rpi-robot-hat]] + 机身 IMU（[[board-imu-to-dxl]] / [[imu-to-dxl-v2]]）可实施
- [ ] 契约：DXL / IMU / 策略接口与官方生态一致（见 [[opensource-coverage]]）

相关：[[microduck-diy]] · [[diy-bom]] · [[dual-imu-board-selection]] · [[board-interconnect]]
