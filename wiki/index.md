# Wiki Index

> **Agent 先读：** [[SCHEMA]] · 本文件 · [[log]]  
> 本 wiki：`microduck-diy/wiki/` · 更新：2026-09-15  
> **目标：** 官方原方案完美复刻 · 官方生态完美适配 · 生态内扩展  
> **现行焦点：** 机身 IMU 固件 [#10](https://github.com/ScrapMeta/microduck-diy/issues/10)（U2D2 台架通过 · ready-for-pm）· HAT TTL [#4](https://github.com/ScrapMeta/microduck-diy/issues/4)

## 现行定稿（优先）

### 机身 IMU · imu-to-dxl v0.3

- [[board-imu-to-dxl]] — 总入口（1 号优先 / 2 号暂缓）
- [[imu-to-dxl-firmware-build]] — **固件编译步骤（agent）**
- [[imu-to-dxl-ref-bom]] — **v0.3 BOM**
- [[imu-to-dxl-ref-schematic]] · [[imu-to-dxl-ref-chip-wiring]] · [[imu-to-dxl-ref-pcb-layout]]
- [[imu-to-dxl-lcsc-order-2026-09-09]] — **v0.3 立创 `SO26090921960`**
- [[imu-to-dxl-lcsc-order-2026-09-05]] — 早期立创订单（对照）

### 装机电控

- [[board-interconnect]] — 装机位置 + DXL 接线（定稿）
- [[body-imu-hat-dxl-power-eval]] — 机身 6 V 经 DXL 回灌 HAT（**不采用** · #9）
- [[elec-three-boards]] — HAT · 机身 IMU · 头（HAT BMI088）
- [[board-hat]] · [[elec-rpi-robot-hat]] — 官方 HAT
- [[hat-solder-kit]] — **HAT 焊接配料 / 波次 / DNP**
- [[hat-dxl-bus-debug]] — HAT TTL 舵机测不通（示波器 + 台供）
- [[dual-imu-board-selection]] — 双 IMU 选型结论
- [[elec-three-board-bom]] — 电子 BOM 合并
- [[elec-hat-lcsc-order-2026-09-05]] — HAT 立创订单

### DIY 工程

- [[microduck-diy]] · [[diy-milestones]] · [[diy-bom]]
- [[zero3w-bench-plan]] — **现行：主控台架规划（2G · SD）**
- [[xl330-cn-bench-kit]] — 舵机台架（✅ 通过；资料后补）
- [[local-workspace-layout]] — **布局真源**
- [[ros2-migration-plan]] — ROS2 并行移植规格（software 范畴）
- [Agent 治理 v0.9](../../docs/agent-governance.md)（基础工程 + llm-wiki · 只常驻 pm · 无 handoff）· 入口 [`AGENTS.md`](../../AGENTS.md)

### 主线执行器 / 采购

- [[xl330-cn-bench-kit]] — 国产启动套件台架（**✅ 通过**；资料后补）
- [[robotis]] · [[dynamixel-xl330]] · [[robotis-xl330-order-2026-09-05]]
- [[seeed-bearings]] · [[fastener-bom-study]]
- [[taobao-diy-procurement-2026-09]]

## 官方 Microduck 参考（精简）

- [[microduck]] · [[opensource-coverage]] · [[imu-to-dxl-v2]]（官方契约，未开源板）
- [[pollen-robotics]] · [[hugging-face]] · [[apirrone]] · [[rhoban]]
- [[mechanical-bom-rl]] · [[print-bom-rl]] · [[better-actuator-models-bam]] · [[bam-identification-bench]]
- [[radxa-zero-3w]] · [[radxa]] · [[np-f550-battery]] · [[imx219-camera]] · [[vl53-tof]]
- [[system-flash-armbian]] · [[firmware-flash-matrix]] · [[bench-power-supply]]
- [[microduck-releases]]

## 归档

非现行 Layer-2：[`_archive/`](_archive/README.md)。`raw/` 不可变 ingest。

## Raw

清单：[_meta/raw-inventory](_meta/raw-inventory.md)
