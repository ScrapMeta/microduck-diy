# Microduck 主控系统镜像（复刻构建）

官方**不发布**整机刷机包。量产/开发路径是：

1. 刷 [Armbian 26.2.1 Minimal](https://www.armbian.com/radxa-zero-3/)（Radxa Zero 3）
2. 跑 `microduck/scripts/provision-board.sh`（见 `microduck/docs/robot/install-dev.md`）

本目录把上述流程打成**可复现的 seed 镜像**：底座仍是官方 Armbian，再注入本仓库的 board 脚本与首启入口。  
**不是** Pollen 签名的量产镜像；daemon 仍走官方签名 release（`install.sh` / `updaterd`）。

## 产出物

| 文件 | 说明 |
|------|------|
| `out/microduck-zero3-*-seed.img.xz` | 可刷 eMMC/SD 的镜像 |
| `out/*.sha256` | 校验 |

底座默认：`Armbian_26.8.1_Radxa-zero3_trixie_vendor_6.1.115_minimal`（清华源）  
（**vendor 6.1** + **trixie**；官方文档写的是 26.2.1，同系列更新点版本，脚本兼容。）

国内默认 URL：  
`https://mirrors.tuna.tsinghua.edu.cn/armbian-releases/radxa-zero3/archive/`

## 构建（Linux / WSL2）

在仓库根旁的本目录执行（需 `sudo`、约 4 GB 磁盘）：

```bash
cd /mnt/d/projects/microduck/microduck-diy/image   # WSL 路径按实际调整
export DUCK_REPO_ROOT=/mnt/d/projects/microduck/microduck   # 相对路径已变，建议显式指定
./build-base-image.sh
```

可选环境变量：

| 变量 | 默认 | 含义 |
|------|------|------|
| `ARMBIAN_URL` | archive 上 trixie vendor minimal | 底座下载地址 |
| `DUCK_REPO_ROOT` | 建议设为工作区 `microduck/` 绝对路径（自此目录起旧默认 `../microduck` 已失效） | 注入脚本的来源 |
| `OUT_DIR` | `./out` | 输出目录 |
| `KEEP_RAW=1` | off | 保留未压缩 `.img` |

## 刷机后

1. 用 [Armbian Imager](https://www.armbian.com/radxa-zero-3/) 或 `dd` / Rufus 写入 Zero 3W。
2. 首次开机用串口或 HDMI 完成 Armbian 账号/Wi‑Fi（若刷写前未在 Imager 里预填）。
3. 有网后二选一：

```bash
# A. 官方一键（推荐，与文档一致）
export DUCK_TOKEN=...   # 仓库私有时需要
sudo sh /opt/microduck/scripts/provision.sh --name duck-01

# B. 首启助手（读 /boot/microduck.env）
sudo nano /boot/microduck.env   # 见 microduck.env.example
sudo systemctl start microduck-firstboot
```

## 与官方差异

- 预置 `/opt/microduck/{scripts,deploy}`，断网也能对照脚本；有网 provision 仍会按 `DUCK_REF` 拉更新。
- 预修 `overlay_prefix=rk3568`、`uart2-m0`，并镜像相机 dtbo 前缀（与 `setup-board.sh` 相同逻辑）。
- **不**预装签名 daemon、**不**预装 GStreamer/rkaiq（体积大且要板级探测）；这些仍由 provision 完成。
- 每块板的 BLE/`--weird-ble` 仍需按 `install-dev.md` 实测。
