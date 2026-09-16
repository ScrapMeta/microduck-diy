---
title: Zero 3W 主控台架测试规划（2G · SD）
created: 2026-09-10
updated: 2026-09-14
type: concept
tags: [sbc, flash, camera, diy]
sources:
  - concepts/system-flash-armbian.md
  - entities/radxa-zero-3w.md
  - entities/imx219-camera.md
confidence: medium
related:
  - radxa-zero-3w
  - system-flash-armbian
  - imx219-camera
  - diy-milestones
  - bench-power-supply
  - board-interconnect
  - elec-rpi-robot-hat
  - xl330-cn-bench-kit
---

# Zero 3W 主控台架测试规划（2G · SD）

> **状态：P0 ✅（#2）· P1 ✅（#5 closed）。** 舵机台架 [#1](https://github.com/ScrapMeta/microduck-diy/issues/1)；HAT DXL [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)。  
> 下一步：P2 接口冒烟（可选）· HAT/DXL（#4）与 `provision` 另单。AE/AWB/色彩由上层软件调。  
> 手头：**Radxa Zero 3W · 2 GB RAM · microSD**（非 Press Kit 1G/eMMC 量产口径；开发路径合法）。  
> 真源：[[radxa-zero-3w]] · [[system-flash-armbian]] · [[imx219-camera]]

## 0. 目标（本轮）

在 **不叠 HAT / 不上整机母线** 的前提下，验证主控能否支撑官方生态后续联调：

| 域 | 要证明什么 |
|----|------------|
| **系统** | Armbian 可启动；SSH；基础包与板级脚本路径清楚 |
| **摄像头** | CSI [[imx219-camera]]（Pi Cam v2）出图 / 流 |
| **功能接口** | 与后续装机相关的板载口可用性（见 §3） |

**非本轮：** HAT 叠装供电、DXL 总线经 HAT、机身 IMU ID 200、完整 `robotd`/`mediad` 量产 provision（可列为后续阶段）。

## 1. 手头与物料

| 项 | 现状 / 需求 |
|----|-------------|
| Zero 3W **2G** | ✅ 在手 |
| 启动介质 | **microSD**（本轮主路径） |
| 5V 供电 | USB-C OTG · 见 [[bench-power-supply]] |
| 网 | Wi-Fi（板载）或 USB 网卡（可选） |
| 相机 | Pi Cam **Module 2 / IMX219**（CSI；已购见 [[diy-bom]] / 淘宝页） |
| FPC | 与 Zero CSI 座匹配的排线 |
| 主机 | 烧录用 PC（Armbian Imager / `dd`） |

与量产差异（记一笔即可）：Press Kit 常写 **1G + eMMC**；本板 **2G + SD** 更利于 DIY 迭代，镜像仍按 Zero 3 / Armbian Minimal。

## 2. 阶段划分

### P0 · 系统（先做）

1. 刷 **Armbian Minimal（Radxa Zero 3）** 或本仓 seed `image/out/microduck-zero3-20260829-seed.img.xz` 到 SD——详见 [[system-flash-armbian]]  
   - **原仓更新 ≠ 必须重打系统盘**；microduck 软件靠日后 `provision` 拉新  
   - **推荐 Armbian Imager**（可选本地 `.img.xz`）；**不推荐 balenaEtcher**（解压损坏风险）  
2. 预填用户 / Wi-Fi（或串口/HDMI 首启）  
3. 上电 → 登录 → `uname -a` / `free -h`（确认约 2G）/ 磁盘为 SD  
4. SSH 稳定；时钟与基础 `apt` 可用  
5.（可选）了解 `provision`；本轮不强制完整装机 provision  

验收：冷启动可 SSH，重启 ≥2 次无砖。

### P1 · 摄像头

1. 断电插好 IMX219 CSI（方向勿反）  
2. 启用 Zero3 RPi Camera v2 设备树 / 官方 IQ 路径（`radxa-zero3-rpi-camera-v2` 等，以镜像文档为准）  
3. 抓一帧或短预览（`rpicam-*` / `v4l2` / 官方 mediad 依赖前的最小命令）  
4. 记录分辨率、是否需 rotate-180（alpha 常倒装）

验收：能稳定出至少一路预览/存图；失败则记 dmesg / 设备树。

### P2 · 功能接口（台架级）

按「后续要接什么」做**冒烟**，不必一次接满外设：

| 接口 | 本轮建议 | 备注 |
|------|----------|------|
| **USB-C OTG** | 供电 +（可选）gadget/主机识别 | 主供电 |
| **40-pin GPIO/I²C/UART** | 用万用表/LED 或短接测 3V3/GND；I²C 扫空总线 | 为 HAT 叠装铺路；**本轮不强制插 HAT** |
| **CSI** | 归入 P1 | |
| **Wi-Fi / BT** | ping 外网；`bluetoothctl` 电源开（可浅测） | 手柄配对可后置 |
| microSD | 读写与剩余空间 | |
| HDMI（若用） | 仅排障用，非装机必需 | |

验收：列出「已验证 / 未测 / 阻塞」表，写入本页笔记。

### P3 · 与官方生态对齐（后续，不阻塞 P0–P2）

- 叠 [[elec-rpi-robot-hat]] + 电池/台架 5V 策略  
- 与已通过的舵机台架 [[xl330-cn-bench-kit]] 汇合到 HAT TTL  
- seed / `provision-board.sh`、daemon 拉取  

## 3. 风险与注意

- **电压：** 板只吃 **5V**；勿直接接 DXL 母线  
- **相机：** 勿用 Module 3（IMX708）；NoIR 可用但色彩偏  
- **散热 / 电流：** 2G 板 + 相机预览时注意 Type-C 供电能力  
- **SD vs eMMC：** 本轮只证明 SD 开发流；量产再迁 eMMC  

## 4. 勾选清单

### P0 系统

- [x] SD 镜像烧录完成（型号/版本记下）— `microduck-zero3-20260829-seed.img.xz` · Armbian Imager
- [x] 启动 + SSH — `hdy@192.168.71.101`
- [x] `free -h` 显示 ~2G
- [x] 重启稳定

### P1 摄像头

- [x] CSI 物理连接正确（排线电压/接插复测）
- [x] 设备树 / 驱动加载 — `imx219` · Model ID `0x0219` · i2c `0x10`
- [x] 出图或短预览成功 — `/dev/video0` NV12 → 本机 JPEG（样张 `microduck-diy/tmp/cam-remote2.jpg`）

### P2 接口

- [x] Wi-Fi（或备选有线）可用 — SSH `192.168.71.101`
- [ ] 40-pin 3V3/GND 确认（HAT 前）
- [ ] （可选）I²C / UART 浅测
- [ ] （可选）BT 适配器 up

### 后补资料

- [x] 镜像确切文件名与 sha / 版本号 — seed `microduck-zero3-20260829-seed.img.xz`
- [x] 相机命令与样张路径 — 见 §5 · `tmp/cam-remote*.jpg`
- [ ] 接口测试原始笔记  

## 5. 实验笔记

#### 2026-09-14

- **P0 关闭 [#2](https://github.com/ScrapMeta/microduck-diy/issues/2)。** 镜像 seed `20260829` + Armbian Imager；SSH/`free`/重启已验收。  
- **P1 关闭 [#5](https://github.com/ScrapMeta/microduck-diy/issues/5)。** CSI 通路通过：`imx219` probe OK；远程 `v4l2-ctl` 抓 NV12，本机 ffmpeg 转 JPEG。  
- 默认固定曝光偏暗、无 AWB 偏绿（板未跑 rkaiq）；**台架验收不阻塞**，软件侧再调。  
- **亚博智能 IMX219 加测通过**（Lot `0x522070` / Chip `0x02b7`；样张 `tmp/cam-yahboom.jpg`）；与首颗同通路、同偏色结论。  
- 板侧：`6.1.115-vendor-rk35xx` · overlays `uart2-m0` + `radxa-zero3-rpi-camera-v2`；空闲约 49–50 °C。  
- HAT/DXL 冒烟已提前摸过（总线未通）；**不计入 P0/P1**。

#### 2026-09-10

- **规划定稿。** 手头 2G+SD；先系统 → 摄像头 → 功能接口。  
- 执行记录后补。

相关：[[radxa-zero-3w]] · [[system-flash-armbian]] · [[imx219-camera]] · [[diy-milestones]] · [[bench-power-supply]]
