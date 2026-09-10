---
title: Better Actuator Models (BAM)
created: 2026-08-30
updated: 2026-08-30
type: entity
tags: [bam, sim2real, mujoco, open-source]
sources: [raw/transcripts/research-hardware-servos-2026-08.md]
confidence: high
---

# BAM（Better Actuator Models）

[[rhoban]] 开源库：用实测轨迹拟合扩展摩擦模型，改善舵机仿真（MuJoCo）。PyPI：`better-actuator-models`。文档：https://bam.readthedocs.io/

## 已有模型（与本域相关）

| 型号 | 有无 |
|------|------|
| Dynamixel XL330-288-T | **有**（Microduck 用） |
| Feetech STS3215 | **有** |
| STS3032 / HL-2915 / HL-3915 | **无** |

## 自己适配

录激励 → 拟合 → 接入 MJCF。需台架与总线驱动；飞特要 STS/HLS 录制脚本。工作量通常 **数天到数周**，不是改配置一行。社区：`zeroth-robotics/bam-feetech`。

Microduck RL 任务大量引用 canonical BAM / `FrictionDRBamActuator`。

相关：[[dynamixel-xl330]] · [[better-actuator-models-bam]] · [[microduck]]
