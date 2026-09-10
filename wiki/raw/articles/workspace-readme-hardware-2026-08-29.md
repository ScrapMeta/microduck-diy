---
source_url: file://D:/projects/microduck/README.md
ingested: 2026-08-30
sha256: 11160bb0dee4d2a3e354c035ecd1e504fcd088ed5dc70b2bf749cd32e002f249
---

# 本地工作区 README — 硬件与烧录节选（2026-08-29）

从 `D:\projects\microduck\README.md` 摘录已确认结论。

## 三块板

| 角色 | 型号 |
|------|------|
| 主控 | Radxa Zero 3W（RK3566）；早期原型 Pi Zero 2W |
| 扩展+电源 | elec_RPI_Robot_HAT（ASE01187-C1） |
| 机身 IMU | imu_to_dxl v2（LSM6DSV16X，DXL ID 200）；**未开源** |

## 接线（公开可确认）

NP-F550 → HAT → 40pin Radxa；Dynamixel 口带 15× XL330 + imu_to_dxl；ToF 经 Qwiic；音频经 AIC3104+PAM8406；摄像头 IMX219 CSI 直连 Radxa。

## 烧录矩阵

- Radxa：刷 Armbian
- HAT：基本无需用户 MCU 烧录
- imu_to_dxl：产线烧 MCU
- XL330：产线写 ID/参数
- ToF：每次 tofd 启动灌 ~90KB 固件到传感器 RAM

## 开源缺口

imu_to_dxl 原理图/固件；整机机械与线束；头部 IMU / NFC 专板；产线舵机配置流程。
