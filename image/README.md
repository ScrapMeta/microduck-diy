# microduck-diy/image — Zero 3W seed 镜像

官方**不发布**整机刷机包。本目录把「Armbian Minimal + board 脚本」打成可复现 **seed**（非 Pollen 签名量产盘）。

## 已有产物（P0 可直接刷）

| 文件 | 说明 |
|------|------|
| [`out/microduck-zero3-20260829-seed.img.xz`](out/microduck-zero3-20260829-seed.img.xz) | 2026-08-29 构建 · ~411 MB |
| `out/*.sha256` | 校验 |

刷写：**推荐 [Armbian Imager](https://imager.armbian.com/)** 选「本地镜像」→ 选上述 `.img.xz` → 写入 microSD。  
**不推荐** balenaEtcher（见 wiki [[system-flash-armbian]]）。

底座默认曾用：`Armbian_26.8.1_Radxa-zero3_trixie_vendor_6.1.115_minimal`（清华源）。

## 重新构建（可选 · Linux/WSL2）

```bash
cd /mnt/d/projects/microduck/microduck-diy/image
export DUCK_REPO_ROOT=/mnt/d/projects/microduck/microduck
./build-base-image.sh
```

`DUCK_REPO_ROOT` 默认相对路径为工作区旁 `microduck/`（`../../microduck`）。大文件 `out/*.img*` **不进 git**。

## 刷机后

见 wiki：[[system-flash-armbian]] · [[zero3w-bench-plan]] · 官方 `microduck/docs/robot/install-dev.md`。
