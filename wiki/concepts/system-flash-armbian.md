---
title: 系统烧录（Armbian / seed）
created: 2026-08-30
updated: 2026-09-10
type: concept
tags: [flash, armbian, emmc, sd]
sources:
  - raw/articles/image-readme-seed-2026-08-29.md
  - ../microduck/docs/robot/install-dev.md
confidence: high
related:
  - radxa-zero-3w
  - zero3w-bench-plan
  - firmware-flash-matrix
  - bench-power-supply
---

# 系统烧录（Armbian / seed）

官方**不发布**整机刷机包。路径始终是：

1. 刷 **Armbian Minimal（Radxa Zero 3）** 到 SD 或 eMMC  
2. 上网后跑 `provision`（装 daemon / 板级脚本）

## 原工程更新了，要不要重打镜像？

| 层 | 谁更新 | P0 要不要重刷底座 |
|----|--------|-------------------|
| **Armbian 底座** | Armbian 发版（如 26.2.1 → **26.8.1** Minimal） | 仅当底座太旧 / 内核驱动缺（相机、vendor 内核）时换新 Minimal |
| **microduck 软件**（robotd、mediad、provision 脚本…） | `pollen-robotics/microduck` 频繁合入 | **一般不重刷系统**；开机后对 **最新 `main`** 跑 `provision` 即可拿到 |
| **本地 seed**（`microduck-diy/image`） | 自建叠加脚本 | 可选；P0 可直接刷已有 `out/*-seed.img.xz` |

**结论（P0）：** 用当前稳定的 **Armbian Minimal · Zero 3 · vendor** 刷一张新 SD 即可。  
仓库近期大量更新 ≠ 必须重打系统盘；那是 provision / 二进制层。若 SD 上已是很旧的 Armbian，建议直接刷新 Minimal，再 provision。

文档仍常写 **26.2.1**；Armbian 站上 Zero 3 现常见 **26.8.1 Minimal（Debian trixie · vendor 6.1）**——同系列 Minimal 即可，记下确切文件名。

## balenaEtcher 可以吗？

| 工具 | 建议 |
|------|------|
| **[Armbian Imager](https://imager.armbian.com/)** | **推荐**（官方 Armbian 文档；可选板型、校验、防误选盘） |
| **balenaEtcher** | **不推荐**（Armbian 文档：解压相关损坏导致坏镜像的报告较多） |
| `dd` / Rufus 等 | 可用；自行校验 sha256 |

若仍坚持 Etcher：先把 `.img.xz` **解压成 `.img`** 再 Flash（Radxa 文档也要求先解压），并仔细核对目标盘。

## 怎么烧（P0 · SD · 推荐流程）

1. 准备 ≥8 GB microSD、读卡器、5V USB-C 供电（[[bench-power-supply]]）  
2. 安装 **Armbian Imager**  
3. 选板：**Radxa Zero 3** → 镜像：**Minimal / CLI**（vendor；优先站点 Recommended）  
   - 或「本地镜像」：选已下载的 `Armbian_*_Radxa-zero3_*_minimal*.img.xz`  
4. 选中 **SD 卡**（勿选电脑硬盘）→ Flash → 等校验结束  
5. （可选）在 Imager 里预填用户名 / 密码 / Wi-Fi  
6. SD 插入 [[radxa-zero-3w]] → Type-C **5V** 上电  
7. SSH 或串口/HDMI 登录 → `uname -a` · `free -h`（约 2G）  
8. **本轮 P0 到此可验收**；装官方栈再：

```bash
# 开发机侧（有网、有 token 时）见 microduck/docs/robot/install-dev.md
./scripts/provision-board.sh user@<board-ip>
```

## SD vs eMMC

- **开发（本轮）：** SD  
- **量产倾向：** eMMC（Press Kit）；可先 SD 启动再 `armbian-install` 迁 eMMC  

本地 seed 复刻：[`microduck-diy/image/`](../../image/)（已有 `out/microduck-zero3-20260829-seed.img.xz`；大文件不进 git）。

相关：[[radxa-zero-3w]] · [[zero3w-bench-plan]] · [[firmware-flash-matrix]] · [[bench-power-supply]]
