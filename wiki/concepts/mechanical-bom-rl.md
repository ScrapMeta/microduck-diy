---
title: RL 机械网格 BOM（robot_walk）
created: 2026-09-01
updated: 2026-09-06
type: concept
tags: [mechanical, bom, mujoco]
sources:
  - ../refs/microduck_rl/src/mjlab_microduck/robot/microduck/robot_walk.xml
confidence: high
related: [print-bom-rl, diy-bom, seeed-bearings, fastener-bom-study]
---

# RL 机械网格 BOM（官方 `robot_walk`）

来源：`refs/microduck_rl/.../robot/microduck/robot_walk.xml` + `assets/`。  
**38 种网格 / 70 个视觉实例**。比 app alpha 网格（34/64，已归档 `_archive/mechanical-bom-alpha`）更新；打印与装配以本页为准。

## 数量表（入结构）

| 数量 | 名称 |
|------|------|
| 15 | `xl330` |
| 11 | `seeed_bearing__configuration__22x16x4` |
| 3 | `seeed_bearing__configuration_default` |
| 2 | `bearing_roll`, `hip_l`, `leg`, `neck`, `upper_leg_rigidity_plate`, `yaw2roll` |
| 1 | `ankle_left/right`, `banana_pcb_locker`, `bottom_head_shell`, `elec_rpi_robot_hat_pcb`, `face_part`, `foot_left/right`, `jaw`, `jaw_soft`, `left_shell`, `lens`, `m12_lens_holder`, `motor_support`, `neck_pitch`, `noenoeil`, `np_f970`, `pcb__raspberry_pi_zero_2_w`, `power_support`, `right_shell`, `soft_mouth_top`, `sole_left/right`, `speaker`, `top_head_shell`, `trunk_base`, `upper_leg_left`, `upper_leg_right`, `yaw_roll_motion` |

轴承规格见 [[seeed-bearings]]。舵机见 [[dynamixel-xl330]]。

## 命名注意

| 结构实际用 | 勿用（磁盘残留） |
|------------|------------------|
| `left_shell` / `right_shell` | `trunk_shell_*` |
| `upper_leg_left` / `upper_leg_right` | `left_upper_leg`；右腿旧 `right_upper_leg` **几何不同** |

## 磁盘有、walk 不用（9）

`ankle_l_v1`, `ankle_r_v1`, `left_upper_leg`, `right_upper_leg`, `rim`, `roller_blade`, `tire`, `trunk_shell_left`, `trunk_shell_right`  
（后五项见 rollers 场景 XML。）

## 版本差（网格 vs 量产）

- 主控网格：Pi Zero 2W → 量产 [[radxa-zero-3w]]
- 电池网格：`np_f970` → [[np-f550-battery]]
- 无 `imu_to_dxl` PCB 网格；仅有 site，见 [[imu-to-dxl-v2]]

相关：[[print-bom-rl]] · [[diy-bom]] · [[microduck-diy]] · [[opensource-coverage]]
