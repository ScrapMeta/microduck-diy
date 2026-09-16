---
title: DIY 里程碑
created: 2026-09-03
updated: 2026-09-15
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
  - dynamixel-xl330
  - xl330-cn-bench-kit
  - zero3w-bench-plan
  - radxa-zero-3w
  - hat-solder-kit
  - hat-dxl-bus-debug
---

# DIY 里程碑

[[microduck-diy]] 的项目阶段用语义化版本号（`v0.x`）标记。过程面：GitHub Issue（治理 [v0.8](../../../docs/agent-governance.md)）。

## 项目目标

1. **完美复刻**官方 [[microduck]] 原方案  
2. **完美适配**官方生态（可对接官方软件栈与总线契约）  
3. 在官方生态下**扩展**硬件与玩法  

v0.1 阶段验收口径（可联调）：主控 + 舵机总线 + 机身 IMU + 供电，并能部署官方行走相关策略。

## 里程碑表

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| **v0.1** | **当前** | 官方方案可复现联调（进行中）· GitHub Milestone `v0.1` |
| v0.2+ | 未开 | v0.1 验收后再定 |

### v0.1 验收（草稿）

- [x] **舵机台架：** [[xl330-cn-bench-kit]] · Issue [#1](https://github.com/ScrapMeta/microduck-diy/issues/1)（**closed** · 2026-09-10 通过；明细后补）
- [x] **主控台架 P0/P1：** [[zero3w-bench-plan]] · [#2](https://github.com/ScrapMeta/microduck-diy/issues/2) / [#5](https://github.com/ScrapMeta/microduck-diy/issues/5)（**closed**）
- [ ] 机械：结构可干装配（打印 / 紧固件 / 轴承 / XL330）
- [x] **HAT 配料焊接：** [[hat-solder-kit]] · Issue [#3](https://github.com/ScrapMeta/microduck-diy/issues/3)（**closed** · 2026-09-14；TTL 联调见 #4）
- [ ] **供电拓扑评估：** Issue [#9](https://github.com/ScrapMeta/microduck-diy/issues/9)（机身≈6 V 经 DXL 3P 供 HAT · 是否稳压）
- [ ] **HAT TTL 舵机：** [[hat-dxl-bus-debug]] · Issue [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)（**blocked** · 等示波器 + 30V10A · 2026-09-15）
- [x] **机身 IMU 固件+U2D2：** Issue [#10](https://github.com/ScrapMeta/microduck-diy/issues/10)（`a49a628` · Ping/Read 1000 + SyncRead 10 min 通过 · **ready-for-pm**）· 零回包 [#7](https://github.com/ScrapMeta/microduck-diy/issues/7) 由 #10 覆盖待 pm 关 · 对照 [#8](https://github.com/ScrapMeta/microduck-diy/issues/8)（replica0908）仍 open · 手册 [[imu-to-dxl-firmware-build]]
- [ ] 电控联调：Zero + HAT + 机身 IMU（[[board-imu-to-dxl]] / [[imu-to-dxl-v2]]）可实施
- [ ] 契约：DXL / IMU / 策略接口与官方生态一致（见 [[opensource-coverage]]）

相关：[[microduck-diy]] · [[diy-bom]] · [[xl330-cn-bench-kit]] · [[board-interconnect]]
