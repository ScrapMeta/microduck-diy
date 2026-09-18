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
| 何时值得搭辨识台？ | CN 批次手感明显偏离、换飞特/无模型舵机、或 train 侧要自建摩擦域随机。**换舵机场景见 §「分阶测试」的决策表**——虚位/柔度型差异做辨识是白费 |
| 与现有舵机台架关系 | [[xl330-cn-bench-kit]]（U2D2+供电）可复用总线/电源；**摆臂+配重+刚底座**另做，勿与整机 HAT 总线混用大电流 |

## 论文与仓库（真源）

- 论文：*Extended Friction Models for the Physics Simulation of Servo Actuators*（arXiv [2410.08650](https://arxiv.org/abs/2410.08650)）— Coulomb-Viscous 不足；扩展模型（Stribeck / 负载相关 / 方向 / 二次等）；单摆轨迹辨识；4 款舵机 + 2R 验证  
- 实现：https://github.com/Rhoban/bam · 文档 setup：https://bam.readthedocs.io/en/latest/identification/setup.html  
- 飞书附件：`bam论文.pdf` / `bam_zh.pdf`（未入库；需组织权限下载）

## 台架 BOM 摘要（社区 §5.1）

**电气：** 总线舵机（可读位置/速度/电压、可写 P、堵转约 ≥0.3 N·m）· DXL→U2D2（或兼容）· 稳压电源（**vin 全程固定并实测**，用 **6.0 V** = 整机运行点）

> **辨识电压必须是 6.0 V（2026-09-18 定案）**：整机母线由降压模块稳在 **6.0 V** 长期运行，
> 而辨识出的模型**对应辨识时的供压**（供压决定可用扭矩与电流爬升：6.0 V → 0.60 N·m，
> 6.5 V 线性外推约 0.65 N·m，差 ~8 %）。**用 6.5 V 辨识 = 模型对应另一个电压点**，
> 装到 6.0 V 的整机上等于换了执行器。**6.5 V 只是台架曾用值，不要用于辨识。**  

**结构：** 不晃底座 · 3D 夹具 · 摆臂 0.10/0.15/0.20 m · 砝码约 0.1–1.0 kg · M3 紧固  

**计量：** 0.1 g 秤 · 卡尺量「轴心→配重质心」· 示波器测 `error_gain` 可选（可用 `error_gain_ratio` 拟合代替）

### 打印件：仓里已有整套（2026-09-18 核实）

`refs/microduck_rl/src/mjlab_microduck/robot/xl330_test_bench/` 下有完整零件表，
由 Onshape 文档导出（链接在 `config.json` 的 `url`）：

| STL | 件 | 数量 | 装配位置（XML） |
|-----|----|------|-----------------|
| `bench_holder.stl` | 底座支架（夹持用）| 1 | `worldbody` 根 |
| `arm.stl` | 摆臂 | **2** | 同名几何在 XML 里出现两次（`arm` + `arm_2`）|
| `spacer.stl` | 隔套 | **2** | 同上 |
| `axis.stl` | 轴 | 1 | — |
| `weight.stl` | 配重 | 1 | 挂在臂端 |
| `xl330.stl` | 舵机占位 | 1 | 仅作装配校对，非打印件 |

**⚠ 这些 STL 是为仿真简化过的，不能直接拿去打印。** `config.json` 里
`"simplify_stls": true` 且 `"max_stl_size": 1.0`（1 MB 上限），`arm.stl` 只有 151 KB
—— 是抽稀后的网格，尺寸与配合精度不足以装机。
**要打印请去 `config.json` 里的 Onshape 原文档导出**；仓内 STL 只用于仿真与目视校对。

### ⚠ 质量真源冲突（上机前必须解决）

仓内两处写着**不同的摆臂质量**：

| 位置 | 值 | 说明 |
|------|-----|------|
| `xl330_test_bench.xml` | `mass="0.1"` | 注释写「Real device has a 100 g payload on the arm」|
| `testbench_constants.py` | `TESTBENCH_ARM_MASS = 0.12` | **120 g，且 `_set_arm_mass()` 会覆盖 XML** |

两者差 **20 %**，而 BAM 的全部意义就是「**质量必须实测、禁用铭牌标称**」（见下「操作硬约束」§2）。
**上机前用 0.1 g 秤称实际那根臂 + 配重，按实测值填 `--mass` / `--arm-mass`。**
这个冲突本身就是该条硬约束要防的东西。

**关节行程**：XML 的 `range="-1.3962634 1.3962634"` = **±80°**，与
`testbench_sim2real.py` 和 `scripts/servo_swap_compare.py` 的 `MAX_ANGLE` **完全一致** ✓

## 操作硬约束

1. **电压恒定**：`--vin` = 实测；中途改压 = 污染数据  
2. **质量/长度必须实测**：`--mass` / `--arm-mass`，禁用铭牌标称  
3. **安全**：配重双螺母；摆平面禁入  
4. **主机**：Linux/WSL + `uv`；录制不重算力  
5. CAD：官方 XL330 Onshape（BAM setup）或 microduck `xl330_test_bench`（见上「打印件」）

## 分阶测试：先空载筛，再上摆臂（2026-09-18）

换舵机（如 [[xl330-vs-kpower-rd05t]]）时**不必一上来就搭单摆台**。台架的用途分两层，
而**第一层不需要负载**：

| 阶段 | 要摆臂吗 | 能回答 | 耗时 |
|------|----------|--------|------|
| **T1 身份** | 否（只要舵机+电源+USB）| `Model Number(0)`、寄存器**可写性**（含 P 增益）| 分钟 |
| **T2 空载 A/B** | **否** | **死区 / 回差 / 迟滞** —— 即「离合」风险 | ~1 小时 |
| **T3 负载 A/B** | **是** | **摩擦对比**（`ramp_slow`）、完整差值之差 | ~1 天 |
| **T4 辨识** | **是** | 新舵机的动力学**能否被建模** | 数天–数周 |

**为何 T2 能省下台架**：`scripts/servo_swap_compare.py` 的 `dead_steps` / `hysteresis` /
`dead_time` 测的是**虚位与柔度**，空载即可显形（输出轴在间隙内自由行程不需要外力）。
只有 `ramp_slow` 的摩擦对比需要配重产生恒定力矩——**空载没有力矩，静摩擦几乎不被激励**。
故 T2 的 `tracking_mae` **不可用于判摩擦**，只用于判虚位。

### 要不要做 T4 辨识：取决于 T2/T3 的**诊断分型**，不取决于「能不能用」

| A/B 结果 | 做 T4 吗 | 理由 |
|----------|----------|------|
| `dead_steps` / `hysteresis` 显著更大 | **不必** | 那是**机械虚位 / 柔度元件**。BAM 拟的是**摩擦**（库仑 + 黏滞 + 负载相关），**表达不了运动学/结构属性** → 投入白费 |
| 只有 `tracking_mae` 大（虚位/迟滞正常）| **值得** | 这是**摩擦或电机参数不同**，正是辨识能修的 |
| 全在容差内 | — | 理论 drop-in，但仍须面对下面的批次问题 |

**顺序**：T2/T3 先做（便宜、约 1 天）→ 再决定 T4（贵、数天–数周）。**别反过来。**

**T4 的电气闸门**：[[bam-identification-bench]] 的电气前提含「**可写 P 增益寄存器**」。
若不成立，**辨识路径直接断掉**，与协议是否兼容无关。**这一步 T1 就能判**，
不必等到 T4 才发现。

### T3/T4 覆盖不到的两件事

1. **批次一致性** —— BAM 是**单台**辨识的。15 台若散布大，模型等于错。
   **1~2 台样本测不出这一项**，必须靠供货保证（PCN / EOL 承诺）。
2. **策略在环** —— 归 `refs/microduck_rl/scripts/testbench_sim2real.py`（同 ONNX 跑 sim 与真机）。

## 缺口

- 飞书 §二–四：公式图为主，本 wiki **不抄图**；以论文/官方文档为准  
- §5.2 实操命令流：待登录飞书补抓，或直接跟 BAM identification 流水线  

相关：[[better-actuator-models-bam]] · [[dynamixel-xl330]] · [[xl330-cn-bench-kit]] · [[rhoban]]
