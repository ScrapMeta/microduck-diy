---
title: microduck 官方 Release 源码归档
created: 2026-09-06
updated: 2026-09-06
type: concept
tags: [runtime, open-source, workspace]
sources:
  - https://github.com/pollen-robotics/microduck/releases
  - raw/assets/microduck-releases/README.md
confidence: high
related: [microduck, opensource-coverage, local-workspace-layout]
---

# microduck 官方 Release 源码归档

本地镜像 [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) 各**稳定版** Release 的 GitHub **Source code (zip)**。

## 存放位置

`wiki/raw/assets/microduck-releases/`  
清单与 SHA256：同目录 [`README.md`](../raw/assets/microduck-releases/README.md)

## 范围（2026-09-06）

| 已归档 | 未归档 |
|--------|--------|
| `daemon-v0.2.0` … `daemon-v0.10.0`（**12** 个稳定 tag） | `-dev` / `staging` 预发布（约 17 个） |

- 归档的是 **源码 zip**，不是机器人 OTA 用的 `daemon-*.tar.zst`。  
- 当前 Latest：**daemon-v0.10.0**（2026-08-27）。本地 clone 的 `main` 可能更新（如 remote-access），以 git HEAD 为准。

相关：[[microduck]] · [[opensource-coverage]] · [[local-workspace-layout]]
