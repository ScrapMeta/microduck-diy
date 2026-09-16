---
title: ROS2 迁移计划与契约
created: 2026-09-16
updated: 2026-09-16
type: concept
tags: [runtime, rl, sim2real, workspace]
sources:
  - concepts/local-workspace-layout.md
related:
  - local-workspace-layout
  - imu-to-dxl-firmware-build
  - diy-milestones
confidence: high
---

# ROS2 迁移计划与契约

> **定位：** ROS2 属 **software** 范畴的并行移植，**不是**独立职能。
> 治理条款见 `.cursor/rules/microduck-ros2.mdc`；本页为**契约摘要**。
> **细节与实施步骤**：`microduck_ros2/docs/ros2-migration-plan.md`（详版规划）·
> `microduck_ros2/docs/phase1-wsl-onnx-sim.md`（一期操作）。
> ⚠️ `microduck_ros2/` **尚未纳入版本控制**——本页是唯一有版本历史的契约记录，改契约先改本页。
> 代码落点：`microduck_ros2/`（colcon 工作区）。

官方量产栈是 Rust `microduck/` + MuJoCo `microduck_rl/`。
ROS2 为**并行移植与扩展**；勿覆盖官方运行时契约，除非用户明确要求。

## 一期（当前优先）

WSL Ubuntu 22 + Humble：MuJoCo + vendored/Spark ONNX @ **50 Hz**，键盘 / `cmd_vel` 控制。

- 契约：**obs 61 → act 14**
- 复用：`microduck_rl/scripts/infer_policy.py`

## 目标平台

- 主控：**RK3576 / RK3588 / RV1126B**（及同类 Rockchip）；官方参考 Radxa Zero 3W（RK3566）
- 系统：Ubuntu 22.04 / 24.04；ROS 2 **Humble / Jazzy**（与发行版对齐）
- 交叉编译与板端 native 构建**都要可复现**；板相关 overlay 放 `microduck_ros2/boards/`

## 能力分层（按优先级交付）

1. **基础**：运动控制（Dynamixel / `cmd_vel` / joint）· 摄像头 · 麦克 · 喇叭 · ToF · IMU
2. **仿真**：URDF/xacro · `robot_state_publisher` · RViz2；与现有 MJCF 关节命名对齐
3. **导航**：SLAM / VSLAM · 定位 · Nav2
4. **视觉扩展**：检测 · 人脸 · 语义分割等（优先 NPU/RGA 友好路径）
5. **远期**：Isaac Sim / Isaac Lab · 本地 LLM 决策与任务规划 · 本地 ASR/TTS / agent

## 工程约定

- ament 包：`microduck_*` 前缀；launch 用 Python；参数用 YAML
- Topic/TF 命名**稳定且文档化**；与 `microduck_maploc_rs` / kinematics 语义可对齐时优先对齐
- 板卡差异用 launch 参数 / 硬件描述包隔离，避免 `#ifdef` 散落业务逻辑
- **不默认改** `microduck_rl` / 官方 daemon；需桥接时单独 `*_bridge` 包

## 参考资产

| 用途 | 路径 |
|------|------|
| 控制 / 舵机 | `microduck/` · `elec_RPI_Robot_HAT/` |
| 模型（MJCF → URDF，保持 14 关节顺序） | `microduck_rl/.../robot/microduck/` |
| ToF / 地图 | `microduck_maploc_rs/` |
| 语音 | `microduck_sounds/` |
| 视觉 | `microduck_pet_detect/` |

相关：[[local-workspace-layout]] · [[diy-milestones]] · [[imu-to-dxl-firmware-build]]
