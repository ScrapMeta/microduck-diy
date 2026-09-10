---
source_url: null
ingested: 2026-08-30
sha256: f85558e2123dcc128b7e3f9920b2deba7a4fddc74328b9f8378aaac07e42b174
---

# 研究会话整理：硬件 / 供电 / 舵机 / BAM（2026-08-29～30）

会话主题（Cursor）：SD 烧录与 BOM、NoIR 相机、台架供电、XL330 vs 飞特、BAM 适配。

## 已确认

1. 系统镜像刷到 Zero 3W 存储；开发常 SD，量产偏向板载 eMMC（Press Kit 32 GB）。
2. 电子 BOM：Radxa + HAT + imu_to_dxl + 15×XL330 + ToF + IMX219 + 喇叭/麦 + NP-F550；头 IMU/NFC 未公开专板。
3. alpha 机械网格：34 种 / 64 实例；螺丝反推以 M2 为主，Pi 孔 M2.5×4。
4. NoIR Cam Module 2（IMX219）电气可用；白天色彩偏；勿用 Module 3（IMX708）。
5. 无电池台架：仅 3W → 5V Type-C（Radxa PD30W）；带舵机 → 7.4V 级台供进 HAT。
6. 飞特：STS3032 最贴 XL330 电气；STS3215 更大一档；HL-2915/3915 为 12V 大扭矩；3915 为铝壳恒力版。
7. BAM（Rhoban）已有 XL330-M288 与 STS3215；无 HL/STS3032；可自建辨识但偏科研。

## 未解决

- imu_to_dxl 公开资料仍无
- 官方机械 CAD / 线束 BOM 未开源
- HL 系列接入 Microduck 软件栈需重写协议与重训
