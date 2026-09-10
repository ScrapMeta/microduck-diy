---
title: 系统烧录（Armbian / seed）
created: 2026-08-30
updated: 2026-08-30
type: concept
tags: [flash, armbian, emmc, sd]
sources:
  - raw/articles/image-readme-seed-2026-08-29.md
confidence: high
---

# 系统烧录

1. Armbian Imager：Radxa Zero 3 → Minimal（文档常写 26.2.1）
2. 预填 Wi-Fi / 用户；ssh 后 `provision-board.sh`
3. 本地复刻：`image/build-base-image.sh` → `*.seed.img.xz`

## SD vs eMMC

- **开发**：刷 SD → 插入 [[radxa-zero-3w]] 常见且可行
- **量产倾向**：板载 eMMC（Press Kit 32 GB；updater 写 Storage is eMMC）
- seed 镜像两种介质都能写；eMMC 可用 Maskrom/USB 工具

相关：[[radxa-zero-3w]] · [[firmware-flash-matrix]] · [[bench-power-supply]]
