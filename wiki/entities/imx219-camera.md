---
title: IMX219 / Pi Camera Module 2
created: 2026-08-30
updated: 2026-08-30
type: entity
tags: [camera]
sources:
  - raw/articles/workspace-readme-hardware-2026-08-29.md
  - raw/transcripts/research-hardware-servos-2026-08.md
confidence: high
---

# IMX219（Pi Cam v2）

前置摄像头，**CSI 直连** [[radxa-zero-3w]]（不经 HAT）。软件/IQ：`radxa-zero3-rpi-camera-v2`、`imx219_rpi-camera-v2_default.json`；mediad 钉 1920×1080。alpha 常倒装 + rotate-180。

## NoIR Module 2

同传感器，可用；白天色彩偏红粉。勿用 Module 3（IMX708）。

相关：[[radxa-zero-3w]] · [[microduck]] · [[system-flash-armbian]]
