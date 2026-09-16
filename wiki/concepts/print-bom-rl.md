---
title: RL 3D 打印清单
created: 2026-09-01
updated: 2026-09-11
type: concept
tags: [mechanical, bom, printing]
sources:
  - concepts/mechanical-bom-rl.md
confidence: high
related: [mechanical-bom-rl, seeed-bearings, microduck-diy, diy-bom, fastener-bom-study]
---

# RL 3D 打印清单

基于 [[mechanical-bom-rl]]。现行 3MF：`cad/`。

## 建议打印 · 硬质（PETG/ASA/结构料）

`left/right_shell`, `top/bottom_head_shell`, `face_part`, `trunk_base`, `motor_support`, `power_support`, `banana_pcb_locker`, `upper_leg_left/right`, `upper_leg_rigidity_plate`×2, `leg`×2, `hip_l`×2, `ankle_left/right`, `foot_left/right`, `neck`×2, `neck_pitch`, `yaw2roll`×2, `yaw_roll_motion`, `jaw`, `m12_lens_holder`, `noenoeil` — 约 **31 件**。

## 建议打印 · 软胶（TPU 90–95A）

`sole_left/right`, `jaw_soft`, `soft_mouth_top` — **4 件**。

## 入结构 · 外购（勿当真机打印）

15× [[dynamixel-xl330]]；[[seeed-bearings]]（11+3）；`bearing_roll`×2；HAT PCB；主控/电池占位；`lens`；`speaker`。

## 四色（Press Kit）

| 配色 | 外壳 | 喙/饰 |
|------|------|-------|
| Cream | `#f7e6cb` | 橙 |
| Graphite | `#6c6a68` | 黄 |
| Lavender | `#bfa9cf` | 黄 |
| Sky | `#a9dbe8` | 橙 |

骨架/支架：石墨灰；软底：深灰/黑 TPU。

## 切片提示

- 优先 `microduck_rl_assembly.3mf` / `_exploded.3mf`（命名对象）
- STL 常见为米制，毫米切片常需 ×1000
- 实心轴承占位：[[seeed-bearings]] 的 `_solid` 件
- **轴承盘（打印件）：** 切片将 **XY Hole Compensation = 0.05**（Bambu / Orca 等；单位 mm），保证轴承能套入舵盘；其它件勿盲目照抄

相关：[[mechanical-bom-rl]] · [[diy-bom]] · [[microduck-diy]] · [[fastener-bom-study]] · [[seeed-bearings]]
