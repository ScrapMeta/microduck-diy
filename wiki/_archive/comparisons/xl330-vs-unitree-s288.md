---
title: XL330 vs Unitree S288
created: 2026-08-31
updated: 2026-08-31
type: comparison
tags: [comparison, servo, dynamixel, unitree]
sources:
  - entities/dynamixel-xl330.md
  - entities/unitree-s288.md
  - raw/transcripts/research-hardware-servos-2026-08.md
confidence: high
---

# XL330 vs Unitree S288 — 能否平替？

**结论：不能平替。** 外形接近、减速比几乎相同，但协议、波特率、供电、ID 与整机软件栈均不兼容。

| 维度 | [[dynamixel-xl330]] M288-T | [[unitree-s288]] YS-342026-S288 |
|------|---------------------------|--------------------------------|
| 外形 | 20×34×26 mm | 20×34×26 mm |
| 重量 | ~18 g | 19.5 g |
| 减速比 | 288.4 : 1 | 288.35 : 1 |
| 电压 | 3.7–6 V（推荐 5 V） | **6.4–12.6 V**（推荐 12.6 V） |
| 协议 | **Dynamixel Protocol 2.0** | **宇树自定义**（20/26 字节包 + CRC32） |
| 波特率 | Microduck 用 **1 Mbps** | **6 Mbps 固定** |
| 总线 ID | 0–252；Microduck 用 10–14 / 20–24 / 30–34 + IMU **200** | **0–14**（最多 16 台） |
| 控制接口 | 寄存器 goal position 等 | 混合力位控（τ, pos, spd, Kp, Kd） |
| 软件 | `robotd` + `rustypot` / `Xl330Controller` | 需宇树协议栈；**无官方 Microduck 支持** |
| 仿真 BAM | **有** XL330-288-T | 无 |
| 同总线 IMU | 与 [[imu-to-dxl-v2]] 共 **DXL 2.0** 总线 | 与 DXL IMU **不能同协议混挂** |

## 为何不能「换颗舵机就行」

1. **协议**：`robotd` 每 50 Hz 对 15 台做 `sync_read` / `sync_write`（Dynamixel 2.0），不是宇树 20 字节命令包。
2. **波特率**：总线锁在 1 Mbps；S288 固定 6 Mbps，且主机 UART 需实测是否稳定。
3. **供电**：量产用 [[np-f550-battery]] 约 7.4–8.2 V 负载下；低于 S288 推荐 12.6 V，高于 XL330 标称上限——换 S288 仍要解决降压/分压或改电源架构。
4. **ID 与设备数**：15 舵机 + 机身 IMU（DXL ID 200）依赖 Dynamixel 生态；S288 仅 0–14 且协议不同。
5. **机械**：外形同档不代表 horn、孔位、线出口与 MJCF/打印件一致，需单独核对。

## 若坚持用宇树舵机

需自建机器人（非「平替」）：新总线驱动、新控制律、新 ID/供电设计、重训或重映射关节、MJCF/结构改孔；**不能**指望刷固件让 `robotd` 直接驱动 S288。

## 对比飞特

与 [[xl330-vs-feetech-servos]] 类似：**都不是 drop-in**；飞特至少还有 STS 总线生态与部分 BAM；S288 与 Microduck 开源栈 **零对接**。

相关：[[unitree-s288]] · [[dynamixel-xl330]] · [[better-actuator-models-bam]] · [[board-interconnect]]
