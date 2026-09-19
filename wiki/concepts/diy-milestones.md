---
title: DIY 里程碑
created: 2026-09-03
updated: 2026-09-19
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

[[microduck-diy]] 的项目阶段用语义化版本号（`v0.x`）标记。过程面：[[tasks]] 台账（GitHub Issue 已冻结只读，见 [`AGENTS.md`](../../AGENTS.md)）。

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

### 物料到位（2026-09-19 现状收拢）

| 物料 | 状态 | 落点 |
|------|------|------|
| 主控 [[radxa-zero-3w]] · 系统镜像 | ✅ 在手 · P0 通过（seed `microduck-zero3-20260829-seed.img.xz`） | [[zero3w-bench-plan]] · [[system-flash-armbian]] |
| 摄像头 | ✅ **2 颗**（Pi Cam V2 ＋ 亚博 IMX219）均 probe / 抓帧通过 | [[imx219-camera]] |
| [[board-hat]] | 首板焊完并冒烟 · **3 块待焊** | [[hat-solder-kit]] |
| 机身 IMU 板 | 焊 **5** 块 · 烧录 **3** 块 | [[board-imu-to-dxl]] |
| 电池 ＋ 充电 | F550 **×2** ＋ 双充（2 位） | [[np-f550-battery]] |
| 降压模块 | ✅ **5 V/15 A ×1 · 6 V/4 A ×2** | [[bench-power-supply]] |
| 舵机 | 两批合计 **15 台** = **闲鱼 14**（5 国产组装 ＋ 9 原厂，预计 **09-21 周一**到）＋ **现有 1**；原厂单 [[robotis-xl330-order-2026-09-05]] **延误**（预计 10 月中旬可能发） | [[diy-bom]] §C |
| ToF · 喇叭 | 在途：VL53**L8CX** · 喇叭 **3525 4 Ω 3 W**（均预计 **09-23 周三**） | [[vl53-tof]] · [[hat-solder-kit]] §6.3 |
| 手柄 | Xbox（在手，待测）· 亚博智能 PS2（待试） | 官方按键表 `refs/microduck/configd/src/pad.rs` |

> 母线运行点 **6.0 V**（电池 → 降压模块 → HAT，长期）——定案见 [[bench-power-supply]] · [[body-imu-hat-dxl-power-eval]]。

### v0.1 验收（草稿）

- [x] **舵机台架：** [[xl330-cn-bench-kit]] · Issue [#1](https://github.com/ScrapMeta/microduck-diy/issues/1)（**closed** · 2026-09-10 通过；基线 2026-09-16 补采）
- [x] **主控台架 P0/P1：** [[zero3w-bench-plan]] · [#2](https://github.com/ScrapMeta/microduck-diy/issues/2) / [#5](https://github.com/ScrapMeta/microduck-diy/issues/5)（**closed**）
- [x] **HAT 配料焊接：** [[hat-solder-kit]] · Issue [#3](https://github.com/ScrapMeta/microduck-diy/issues/3)（**closed** · 2026-09-14；TTL 联调见 #4）
- [x] **HAT TTL 舵机：** [[hat-dxl-bus-debug]] · [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)（**closed 2026-09-16** · 原症状不成立，HAT TTL 已通）· 续 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)（`0x55` 帧异常定论 · 波形 · 上总线值 · 限流实测）
- [x] **机身 IMU 固件+U2D2：** Issue [#10](https://github.com/ScrapMeta/microduck-diy/issues/10)（`a49a628` · Ping/Read 1000 + SyncRead 10 min 通过）· 零回包 [#7](https://github.com/ScrapMeta/microduck-diy/issues/7) 由 #10 覆盖 · 对照 [#8](https://github.com/ScrapMeta/microduck-diy/issues/8)（replica0908）仍 open · 手册 [[imu-to-dxl-firmware-build]]
- [x] **供电拓扑评估：** Issue [#9](https://github.com/ScrapMeta/microduck-diy/issues/9) —— **不采用** DXL 回灌；改电池经降压模块稳 6.0 V
- [ ] **整机装配 ＋ 供电链路：** 主控 / HAT / 降压模块 / 电池叠装 · 母线 6.0 V 长期跑得住
- [ ] **多板复现：** 另 **3 块 HAT** 焊完并过 [[hat-solder-kit]] §4 分步测试
- [ ] **官方软件联调：** HAT ＋ 机身 IMU ＋ 1 舵机（麦 / 喇叭出声）
- [ ] **闲鱼批到货 → 装机：** 15 台舵机清点 ＋ ID 图配置 ＋ 整机调试
- [ ] 机械：结构可干装配（打印 / 紧固件 / 轴承 / XL330）· 机身 IMU 改竖装 `power_support` 背板
- [ ] 契约：DXL / IMU / 策略接口与官方生态一致（见 [[opensource-coverage]]）

相关：[[microduck-diy]] · [[diy-bom]] · [[xl330-cn-bench-kit]] · [[board-interconnect]]
