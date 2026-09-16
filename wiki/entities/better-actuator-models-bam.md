---
title: Better Actuator Models (BAM)
created: 2026-08-30
updated: 2026-09-11
type: entity
tags: [bam, sim2real, mujoco, open-source]
sources:
  - raw/transcripts/research-hardware-servos-2026-08.md
  - raw/articles/feishu-bam-identification-zuchuanid-2026-09-08.md
confidence: high
related: [rhoban, dynamixel-xl330, bam-identification-bench, microduck]
---

# BAM（Better Actuator Models）

[[rhoban]] 开源库：用实测轨迹拟合扩展摩擦模型，改善舵机仿真（MuJoCo）。PyPI：`better-actuator-models`。文档：https://bam.readthedocs.io/ · 仓：https://github.com/Rhoban/bam

论文：*Extended Friction Models…*（arXiv [2410.08650](https://arxiv.org/abs/2410.08650)）。

## 已有模型（与本域相关）

| 型号 | 有无 |
|------|------|
| Dynamixel XL330-288-T | **有**（Microduck 用） |
| Feetech STS3215 | **有** |
| STS3032 / HL-2915 / HL-3915 | **无** |

## 自己适配

录激励 → 拟合 → 接入 MJCF。需单摆台架与总线驱动；飞特要 STS/HLS 录制脚本。工作量通常 **数天到数周**，不是改配置一行。社区：`zeroth-robotics/bam-feetech`。

DIY 台架要点与社区笔记合入：[[bam-identification-bench]]。

Microduck RL 任务大量引用 canonical BAM / `FrictionDRBamActuator`。**有现成 XL330 模型时，默认先用库内模型，不必立刻自辨识。**

相关：[[dynamixel-xl330]] · [[bam-identification-bench]] · [[rhoban]] · [[microduck]]
