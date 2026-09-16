---
title: BAM 辨识台架（社区笔记）
created: 2026-09-11
updated: 2026-09-11
type: concept
tags: [bam, sim2real, servo, diy]
sources:
  - raw/articles/feishu-bam-identification-zuchuanid-2026-09-08.md
  - https://arxiv.org/abs/2410.08650
  - https://bam.readthedocs.io/en/latest/identification/setup.html
confidence: medium
related:
  - better-actuator-models-bam
  - dynamixel-xl330
  - xl330-cn-bench-kit
  - rhoban
---

# BAM 辨识台架（社区笔记）

群内「祖传 id」飞书整理：[舵机 bam 辨识](https://gcnvd4jppar0.feishu.cn/wiki/PnuowRaC4iXpNAkmNABclgEwnQd)（2026-09-08）。理论复述论文 + BAM 仓，**可执行价值在 §五工具清单与注意事项**；§5.2 实操步骤飞书页为空，须对照官方文档补全。

## 结论（对本 DIY）

| 问题 | 判断 |
|------|------|
| Microduck 主舵机要不要先自辨识？ | **默认否。** [[better-actuator-models-bam]] 已有 **XL330-288-T**；官方 RL 用 canonical 模型即可 |
| 何时值得搭辨识台？ | CN 批次手感明显偏离、换飞特/无模型舵机、或 train 侧要自建摩擦域随机 |
| 与现有舵机台架关系 | [[xl330-cn-bench-kit]]（U2D2+供电）可复用总线/电源；**摆臂+配重+刚底座**另做，勿与整机 HAT 总线混用大电流 |

## 论文与仓库（真源）

- 论文：*Extended Friction Models for the Physics Simulation of Servo Actuators*（arXiv [2410.08650](https://arxiv.org/abs/2410.08650)）— Coulomb-Viscous 不足；扩展模型（Stribeck / 负载相关 / 方向 / 二次等）；单摆轨迹辨识；4 款舵机 + 2R 验证  
- 实现：https://github.com/Rhoban/bam · 文档 setup：https://bam.readthedocs.io/en/latest/identification/setup.html  
- 飞书附件：`bam论文.pdf` / `bam_zh.pdf`（未入库；需组织权限下载）

## 台架 BOM 摘要（社区 §5.1）

**电气：** 总线舵机（可读位置/速度/电压、可写 P、堵转约 ≥0.3 N·m）· DXL→U2D2（或兼容）· 稳压电源（**vin 全程固定并实测**，如 7.4 V）  

**结构：** 不晃底座 · 3D 夹具 · 摆臂 0.10/0.15/0.20 m · 砝码约 0.1–1.0 kg · M3 紧固  

**计量：** 0.1 g 秤 · 卡尺量「轴心→配重质心」· 示波器测 `error_gain` 可选（可用 `error_gain_ratio` 拟合代替）

## 操作硬约束

1. **电压恒定**：`--vin` = 实测；中途改压 = 污染数据  
2. **质量/长度必须实测**：`--mass` / `--arm-mass`，禁用铭牌标称  
3. **安全**：配重双螺母；摆平面禁入  
4. **主机**：Linux/WSL + `uv`；录制不重算力  
5. CAD：官方 XL330 Onshape（BAM setup）或 microduck `xl330_test_bench`

## 缺口

- 飞书 §二–四：公式图为主，本 wiki **不抄图**；以论文/官方文档为准  
- §5.2 实操命令流：待登录飞书补抓，或直接跟 BAM identification 流水线  

相关：[[better-actuator-models-bam]] · [[dynamixel-xl330]] · [[xl330-cn-bench-kit]] · [[rhoban]]
