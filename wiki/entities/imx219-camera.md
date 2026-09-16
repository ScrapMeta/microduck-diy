---
title: IMX219 / Pi Camera Module 2
created: 2026-08-30
updated: 2026-09-14
type: entity
tags: [camera]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/transcripts/research-hardware-servos-2026-08.md
  - concepts/zero3w-bench-plan.md
confidence: high
---

# IMX219（Pi Cam v2）

前置摄像头，**CSI 直连** [[radxa-zero-3w]]（不经 HAT）。软件/IQ：`radxa-zero3-rpi-camera-v2`、`imx219_rpi-camera-v2_default.json`；mediad 钉 1920×1080。alpha 常倒装 + rotate-180。

## 台架（2026-09-14）

[[zero3w-bench-plan]] P1 / Issue #5 **通过**：probe `0x0219`，`/dev/video0` 可抓 NV12。无 rkaiq 时固定曝光偏暗、缺 AWB 偏绿 → 上层软件调。  
另测 **亚博智能** IMX219 同结论（Chip `0x02b7`；`tmp/cam-yahboom.jpg`）。

## NoIR Module 2

同传感器，可用；白天色彩偏红粉。勿用 Module 3（IMX708）。

相关：[[radxa-zero-3w]] · [[microduck]] · [[system-flash-armbian]] · [[zero3w-bench-plan]]
