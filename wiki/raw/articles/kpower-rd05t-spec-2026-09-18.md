---
source_url: file://c:/Users/Intel/Downloads/Kpower-RD05T-6kg双轴塑胶微型舵机规格书-26-96248d6a90000000010009128.63f2107b000000000f0120e5.1eaabefa94f9c1c.pdf
ingested: 2026-09-18
sha256: f0e4f976b4d179417a8ede336c26ae8b8000a4a08e3369e15524770454fe2f48
note: 供应商规格书（东莞市伟创动力科技有限公司 / Kpower Technology）。PDF 原文件已随仓存档 raw/assets/kpower-rd05t/
---

# Kpower RD05T 规格书 ingest

> raw ingest（只增不改）。Layer-2：[[xl330-vs-kpower-rd05t]]。
> 原件：`raw/assets/kpower-rd05t/RD05T-datasheet-2026-09-18.pdf`（3 页 · 790 KB · sha256 见上）。
> 附图渲染：`RD05T-datasheet-p1.png`（产品图）· `RD05T-drawing-2d.png`（第 3 页 2D 图 + 配件）。

**解码方式**：PDF 表格在纯文本抽取下会被抽平，本页数值由 **PyMuPDF（`fitz`）按坐标分组**还原
（`page.get_text("words")` + 按 y 归行 + 按 x 排序），逐行与原文 y 坐标对齐。数值列有两档：
**@6 V** 与 **@5 V**（表头 `Operating Voltage: V  6  5`）。

## 1. 基本信息（p1）

| 项 | 值 |
|----|-----|
| 型号 | **RD05T** · 6kg 双轴微型机器人舵机 |
| 厂商 | 东莞市伟创动力科技有限公司（Kpower Technology Co., Ltd.） |
| 应用 | 机械臂、仿生机器人、教育机器人 |
| 特性 | 主副**双舵盘**设计 · 精密调齿加工 · **支持过载离合设计** |

## 2. 性能参数 Performance Specification（p1）

| 中文 | 英文 | 单位 | 值 |
|------|------|------|-----|
| 控制协议 | Control System | / | PWM · TTL/RS-485 · CAN/CAN-open（三选一） |
| 马达类型 | Motor | / | DC Brushed Motor |
| 角度传感器 | Position Sensor | / | Magnetic Encoder @360° |
| 外观尺寸 | Dimension (L*W*H) | mm | **26×20×34** |
| 重量 | Weight | g | **18** |
| 工作电压范围 | Operating Voltage Range | V | **3.6～6.0** |
| 典型工作电压 | Operating Voltage | V | **6** ｜ **5** |
| 堵转扭矩 | Stall Torque | kgf·cm | **6** ｜ **5.2** |
| 堵转电流 | Stall Current | mA | **1740** ｜ **1470** |
| 额定扭矩 | Rated Torque | kgf·cm | **1.5** ｜ **1.2** |
| 空载速度 | No Load Speed | sec/60° | **0.08** ｜ **0.1** |
| 空载电流 | No Load Current | mA | **280** ｜ **260** |
| 静态电流 | Idle Current | mA | **10** ｜ **10** |
| 工作角度范围 | Travel Angle Range | ° | **360°** |
| 定位精度 | Position Accuracy | ° | **/（未标）** |
| 连续多圈旋转 | Continuous Rotation | / | **n/a** |
| 齿轮虚位 | Gear Backlash | ° | **/（未标）** |
| 回中差 | Centering Deviation | ° | **/（未标）** |
| 旋转方向 | Rotating Direction | / | **CW** |
| 负载寿命 | Loaded Lifespan | cycle | **＞200,000** |

## 3. 控制特性 Control Specification（p2）

| 中文 | 英文 | 单位 | 值 |
|------|------|------|-----|
| 协议类型 | Protocol Type | / | **TTL (Half Duplex)** ｜ **8 bit, 1 stop, No parity** |
| ID 范围 | ID Range | / | **0 ~ 253** ｜ Customizable |
| 波特率 | Baud Rate | bps | **9600 ~ 4M** |
| 角度传感器分辨率 | Encoder Resolution | ° | **0.088** [deg/pulse] |
| 信号电平 | Signal Voltage | V | High: **2.4 ~ 5.5** ｜ Low: **−0.3 ~ 0.9** |
| 反馈 | Feedback | / | Position · Current · Speed · Input Voltage · Temperature |
| 电子保护 | Electronic Protection | / | Over Load · Over Voltage · Over Current · Over Heat |

## 4. 其他参数 / 连接器（p2）

| 中文 | 英文 | 值 |
|------|------|-----|
| 端子 | Connector | **EH2.54-3P** |
| 线长度 | Length | **180±10 mm** |
| 外壳材质 | Housing Material | **Plastic** |
| 齿轮材质 | Gear Material | **POM** |
| 轴承 | Bearing | **/（未标）** |
| 花键 | Horn Gear Spline | **/（未标）** |
| 输出轴螺丝 | Shaft Screw | **M2.5x5** |
| 噪音 | Noise Level | **60±5 dB @50cm** |
| 运行温度 | Operating Temp Range | **−10 ~ 70 °C** |
| 防护等级 | IP Rating | **IP4X** |
| 认证 | Certifications | RoHS · CE · FCC · UL · ASTM F963 · EN71 · REACH · FDA |

## 5. 规格书**未给出**的关键项（对本项目最重要）

推理结论所依赖、但规格书**完全没有**的项：

| 缺项 | 为什么关键 |
|------|-----------|
| **寄存器地址表 / 协议手册** | 只给了物理层（TTL 半双工 + 8N1）。协议 = 地址表；无表则无法与 DXL 2.0 对照 |
| **工作模式** | XL330 有 6 种（含 Current-based Position / PWM / Extended Position）；本文档一个未列 |
| **减速比** | XL330 = 288.4:1；决定折算惯量（∝N²）与扭矩-转速曲线形状 |
| **内部 PID 增益是否可写** | [[bam-identification-bench]] 的**硬前提**；不可写则无法辨识 |
| **过压/过流/过热阈值与锁存语义** | 决定母线 6.0–6.5 V 下会不会误触发 |
| **定位精度 / 回中差 / 齿轮虚位** | 零位一致性与关节回差；直接影响本体感知 |
| **花键齿数** | 决定能否套用 XL330 舵盘与现有打印件 |
| **减速比 / 堵转扭矩的测试条件** | 未见「持续扭矩 / 占空比」口径 |

> 末尾原文：**「支持定制：舵机的线长、控制协议及性能参数可根据需求进行调整」** —— 即
> **同一外壳可配不同固件**，规格书不构成「到手的这一颗」的协议保证。

## 6. 未做的验证

- 未取得 Kpower 的协议/寄存器手册（官网未公开）
- 未对实物做寄存器读取（无实物）
- 未核对花键齿数与副输出轴尺寸（2D 图为位图，本页仅存档渲染）
