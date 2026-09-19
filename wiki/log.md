# Wiki Log

> Chronological record of all wiki actions. Append-only.  
> Format: `## [YYYY-MM-DD] action | subject`

## [2026-09-16] bench | #4 远程复测 · HAT TTL 打通 · 修脚本 CRC 作用域
- 远程 SSH 进 Zero（`192.168.71.101`，只读检查 + 只读扫总线），HAT **已打通**
  - 软件面全过：`/dev/ttyS2` 在 · `hdy` 在 `dialout` · `serial-getty@ttyS2` **masked**/inactive · `fuser` rc=1 · `overlays=uart2-m0` + `overlay_prefix=rk3568` · `armbianEnv.txt` `console=display` 且 `/proc/cmdline`=`console=tty1`（**本次运行已生效**）
  - **1 Mbps 全静默 → 57 600 上 ID 1 应答**（model 1200）→ §1.1 出厂回退是**唯一命中路径**
  - **发现脚本两个真 bug（已修）**：
    1. **CRC 漏 4 字节 header**（`FF FF FD 00` 起才对）→ 报文被舵机**全部丢弃**；`self-test` 的假舵机**照抄同一错误**故自检全绿 → 第一次台架扫描**两档全「无回包」**，是**假阴性**。现由公开向量 `ff ff fd 00 01 03 00 01 19 4e` 钉死作用域
    2. 本套件回包**多一固定字节 `0x55`**（`LEN = DATA + 4`，规格 +3），**在线上且被舵机 CRC 覆盖**（14/14 帧 `want==got`）；按规格解析得 `error=0x55` 且**所有寄存器整体错位一字节**（`model=45056`、`1792.0 V` 这类「合理但错误」值）。脚本按已知回包长度自动判别两种帧 + 实测帧回放回归
  - `pyserial`/`pip` 在板子上**都没有** → 脚本加 **stdlib `termios` 后端**（Linux 零依赖）；用 PTY 对做 TX+RX 端到端验证
  - 修前/修后台架对照：`error=0x55`+错位值 → `model 1200`/`fw 53`/`shutdown 53`/`5.8 V`/`26 °C`（**与手册出厂默认逐项吻合**）
- **M3 缺口关闭**：基线**已采集**（出厂 ID 1 · 57 600 · fw 53 · `shutdown 53` · 5.8 V）→ 同时**证伪 #1 的「1 Mbps + 同一颗」前提**（该舵机**从未被写过**）
- 实测 `shutdown=53` 直接坐实 [[dynamixel-xl330]] 的订正：出厂 53 **含** InputVoltage 位，`robotd` 的 52 才**清掉**它
- Updated: [[hat-dxl-bus-debug]] §7 · [[dxl-bench-method]] §5.1 §6 §7 · [[xl330-cn-bench-kit]] · [[index]] · `scripts/README.md` · `scripts/dxl_ping.py`
- **未定论**：`0x55` 字节来源（需 U2D2 + Wizard 交叉验证）· 示波器波形 · 写 ID/波特率（归 `robotd`/Wizard）

## [2026-09-15] bench | #10 imu-to-dxl 固件 U2D2 验收
- Commit `a49a628` · Issue [#10](https://github.com/ScrapMeta/microduck-diy/issues/10) · label `ready-for-pm`（待 pm 关单）
- U2D2 COM7：Ping/Read(124,12) 各 1000 · GroupSyncRead ~50 Hz × 10 min（30000 ok · 0 timeout/ShortRead）· @136=`0x03`
- Wiki：[[imu-to-dxl-firmware-build]] §7 · [[board-imu-to-dxl]] · [[diy-milestones]] · [[index]]
- #7 零回包由 #10 覆盖；#8 replica 对照仍 open

## [2026-09-15] issue | #9 机身供电经 DXL 回灌 HAT 评估
- [#9](https://github.com/ScrapMeta/microduck-diy/issues/9) **open**：机身取电→约 6 V（是否稳压）→ DXL 3P 给 HAT；对照现行「电池先进 HAT」
- assignee：hardware 主评 · pm 收口；不阻塞 #4/#7/#8 通信排障

## [2026-09-15] issue | #8 replica0908 焊接 + U2D2 对照
- [#8](https://github.com/ScrapMeta/microduck-diy/issues/8) **open**：焊 replica0908，同 U2D2 看是否与 #7 同为零回包
- 装机仍不采用 45×22；PHY 2G241 ≠ v0.3 1G125
- Open 现行：#4 · #7 · #8

## [2026-09-15] issue | #6 部分关 · #7 零回包排查
- [#6](https://github.com/ScrapMeta/microduck-diy/issues/6) **closed**：GPIOA IOPORT 已修并烧录；U2D2 仍不通不计入本单
- [#7](https://github.com/ScrapMeta/microduck-diy/issues/7) **open**：imu-to-dxl v0.3 U2D2 zero-reply · Milestone v0.1 · sw/hw/bench
- Open 现行：#4 HAT TTL · #7 IMU U2D2

## [2026-09-14] create | imu_to_dxl 固件编译手册
- Concept: [[imu-to-dxl-firmware-build]] — WSL 工具链 · `make host-test` / `make g031` · 产物路径 · 可选 OpenOCD
- Updated: [[board-imu-to-dxl]] · [[firmware-flash-matrix]] · [[index]]

## [2026-09-14] close | Issue #3 HAT 配料焊接
- GitHub: https://github.com/ScrapMeta/microduck-diy/issues/3 · **closed**（completed）
- 用户确认：焊接/基本上电冒烟通过；TTL 舵机不通改由 #4
- Wiki：[[hat-solder-kit]] · [[diy-milestones]]

## [2026-09-14] note | 亚博 IMX219 加测通过
- 同 P1 通路：Model `0x0219` · Lot `0x522070` · Chip `0x02b7` · 样张 `tmp/cam-yahboom.jpg`
- Wiki：[[zero3w-bench-plan]] · [[imx219-camera]]；#5 已 closed，不另开单

## [2026-09-14] close | Issue #5 Zero 3W P1 相机台架
- GitHub: https://github.com/ScrapMeta/microduck-diy/issues/5 · **closed**（completed）
- 证据：I2C `0x10` · Model ID `0x0219` · NV12→本机 JPEG（`tmp/cam-remote2.jpg`）；AE/AWB 留给软件
- Wiki：[[zero3w-bench-plan]] P1 勾选

## [2026-09-14] create | Issue #5 Zero 3W P1 相机台架
- GitHub: https://github.com/ScrapMeta/microduck-diy/issues/5 · Milestone `v0.1` · IMX219 CSI 抓帧
- Wiki：[[zero3w-bench-plan]] 状态指向 #5

## [2026-09-14] close | Issue #2 Zero 3W P0 系统台架
- GitHub: https://github.com/ScrapMeta/microduck-diy/issues/2 · **closed**（completed）
- 镜像：`microduck-zero3-20260829-seed.img.xz` · Armbian Imager；SSH/`free`/重启已验收
- Wiki：[[zero3w-bench-plan]] P0 勾选

## [2026-09-15] observe | XL330 母线电压：7.2 V 持续闪灯 / 6.5 V 正常
- 写入 [[body-imu-hat-dxl-power-eval]] · [[dynamixel-xl330]]：DIY 建议 **6.0–6.5 V** 粗线进 HAT；NP-F 直供需机身 buck

## [2026-09-15] decide | #9 机身 DXL 回灌 HAT 不采用
- Concept: [[body-imu-hat-dxl-power-eval]] — 可行但载流/穿堂风险高；**装机不采用**；6 V 台架可用粗线进 `+BATT`
- [[board-interconnect]] / [[index]] 指针；Issue [#9](https://github.com/ScrapMeta/microduck-diy/issues/9)

## [2026-09-14] create | Issue #4 HAT TTL 舵机 bring-up
- GitHub: https://github.com/ScrapMeta/microduck-diy/issues/4 · Milestone `v0.1` · blocked 至设备到位
- Wiki：[[hat-dxl-bus-debug]] · [[diy-milestones]]

## [2026-09-14] create | HAT TTL 舵机测不通排查
- Concept: [[hat-dxl-bus-debug]] — U2D2 对照 · 7.4 V/1 A · getty/console · 双通道 DATA+DIR
- Linked: [[hat-solder-kit]] §4.8 · [[index]]

## [2026-09-14] update | HAT 不用 485 的焊接清单
- [[hat-solder-kit]] §6.4：可省 U8 / J3 / J11 / R40；**R29、C15 必留**（RO 上拉 + 3V3 去耦）
- [[board-hat]] §5 指向该节

## [2026-09-13] update | HAT 正面贴完分步测试
- [[hat-solder-kit]] §4：目视 → 短路 → 只 HAT 5V → 叠 Zero → i2c 0x18 → 喇叭/麦 → DXL 单舵机

## [2026-09-12] update | HAT 双面焊：二次受热与风枪温度
- [[hat-solder-kit]] §3.3：底面可能脱落；正面用低温锡；风枪 SnBi 约 260–300 °C

## [2026-09-12] update | HAT 底面改加热焊台一次回流
- [[hat-solder-kit]] §3.2：bottom 锡膏 + 加热焊台整面回流；J4 仍后焊；top 夹具风枪

## [2026-09-12] update | HAT 焊接工艺（底烙铁 / 顶风枪）
- [[hat-solder-kit]] §3：按 POS 标注 top/bottom；**J4 在 bottom**；难 IC 多在底面
- 工艺：底面阻容烙铁 + IC 风枪 → **暂缓 J4** → 夹具风枪顶面 → 最后 J4

## [2026-09-12] create | HAT 焊接配料
- Concept: [[hat-solder-kit]] — 开焊闸门 · DNP · 四波次配料 · 上电前检查
- Updated: [[index]] · [[diy-milestones]] · [[diy-bom]] · [[elec-hat-lcsc-order-2026-09-05]]
- Note: wiki 仍无 HAT 空板打板订单记录；开焊前先确认 PCB01186-C1 在手

## [2026-08-30] create | Wiki initialized
- Domain: Microduck 产品 / 硬件 / 舵机 / BAM / 本地工作区
- Structure: SCHEMA.md, index.md, log.md, raw/, entities/, concepts/, comparisons/, queries/, _meta/
- Path: `D:\\projects\\microduck\\wiki`

## [2026-08-30] ingest | 前期研究与官方摘录（batch）
- Raw: fact-sheet, workspace README 硬件节, image seed README, HAT README, research transcript
- Entities (20): companies, Microduck, boards, servos, sensors, BAM
- Concepts (7): interconnect, flash, power, firmware matrix, opensource, mechanical BOM, workspace
- Comparisons (2): XL330 vs Feetech; HL-2915 vs HL-3915
- Query: prior-research-digest-2026-08-30
- Index total pages: 32

## [2026-08-30] ingest | 嘉立创 EDA MCP 调研与接入
- Installed Cursor extension: `chengbin.jlceda-mcp-hub` v1.5.4
- Raw: `raw/articles/jlceda-mcp-hub-readme-2026-08-30.md`
- Concepts: [[jlceda-mcp-setup]], [[imu-schematic-feasibility]]
- Finding: Hub+Bridge can assist reference schematics; cannot reverse closed imu_to_dxl without more data
- Blocker: EasyEDA Pro + MCP Bridge not detected on this machine
- Index total pages: 34

## [2026-09-01] create | dual-imu-board-selection
- Concept: [[dual-imu-board-selection]] — body DXL imu_to_dxl vs head I2C module
- Core: LSM6DSV16X + STM32G0 + HV LDO for board A; I2C LSM6/BMI088 for board B
- Index total pages: 35

## [2026-08-31] ingest | Unitree S288 舵机调研
- Entities: [[unitree]], [[unitree-s288]]
- Comparison: [[xl330-vs-unitree-s288]] — 结论：不能平替 XL330（协议/波特率/电压/软件）
- Index total pages: 37

## [2026-09-01] update | RL 模型/配件/打印/紧固件入库
- Concepts: [[mechanical-bom-rl]], [[print-bom-rl]], [[seeed-bearings]], [[fastener-bom-study]]
- Entity: [[microduck-diy]]
- Updated: [[mechanical-bom-alpha]]（指向 RL）, [[imu-to-dxl-v2]]（site 位姿）, [[local-workspace-layout]]
- Index total pages: 42

## [2026-09-01] create | dual-imu-board-selection
- Concept: [[dual-imu-board-selection]] — body DXL imu_to_dxl vs head I2C module
- Core: LSM6DSV16X + STM32G0 + HV LDO for board A; I2C LSM6/BMI088 for board B
- Index total pages: 43

## [2026-09-01] update | IMU site Viewer 占位 GLB
- ~~Files in `txt2cad/microduck_view/`~~（路径已废弃，见 2026-09-07）
- Documented on [[imu-to-dxl-v2]]

## [2026-09-01] ingest | fanhao375/microduck-replica 书签（不并入主 wiki）
- Raw only: `raw/articles/microduck-replica-fanhao375-2026-09-01.md`
- Source: https://github.com/fanhao375/microduck-replica
- Updated: `_meta/raw-inventory.md`
- Explicitly **not** merged into entities/concepts/index Layer-2 pages

## [2026-09-03] create | DIY 工程版本与里程碑
- Entity update: [[microduck-diy]] — 当前 **v0.1**；目标=官方基础功能；工程↔wiki 同步约定
- Concept: [[diy-milestones]] — v0.1→v0.5 版本线与 M1–M4 验收
- Updated: [[local-workspace-layout]]、[[SCHEMA]]（标签 `diy`）、[[index]]
- Index total pages: 44

## [2026-09-03] update | DIY 项目管理纠正（里程碑≠day）
- 对齐工程仓：目标 / **里程碑 v0.x** / **日志 day*** 三分开
- [[diy-milestones]]：去掉 day↔版本绑定与 v0.1→v0.5 预绑阶梯；**v0.1=当前里程碑**
- [[microduck-diy]]：day* 仅作日志索引，不表示阶段
- Updated: [[index]]、[[local-workspace-layout]]

## [2026-09-03] create | DIY BOM 汇总
- Concept: [[diy-bom]] — 手搓小小鸭 **v0.1** 打印 30+4、轴承 11+3、舵机×15、紧固件示意、M2 电控最小集
- Updated: [[microduck-diy]]、[[diy-milestones]]、[[print-bom-rl]]、[[mechanical-bom-rl]]、[[index]]
- Index total pages: 45

## [2026-09-03] update | XL330 法兰螺丝规格
- [[dynamixel-xl330]] 官方装箱：horn = **PHS M2×6 TAP**×6；frame = **PHS M2×8 TAP**×10
- Updated: [[fastener-bom-study]]、[[diy-bom]]

## [2026-09-03] update | diy-bom 写入舵机螺丝说明
- [[diy-bom]] §C：法兰钉 PHS M2×6 TAP（90）与框架钉 PHS M2×8 TAP（150）入表，附 PHS/TAP 说明

## [2026-09-03] update | imu-to-dxl-ref-schematic 重写
- [[imu-to-dxl-ref-schematic]]：去掉 MCP/改位号/进度流水；仅保留终态 BOM、网络名、分块接线图（电源/DXL/SPI/SWD/LSE DNP）
- 时钟结论：TSSOP-20 无 HSE；主钟 HSI；Y1=32.768 kHz LSE DNP

## [2026-09-03] create | imu-to-dxl-ref-chip-wiring
- Concept: [[imu-to-dxl-ref-chip-wiring]] — U1/U2/U3/U6/Y1/J1/J2 线框接线图
- Linked from [[imu-to-dxl-ref-schematic]]；拆页以遵守 ≤200 行

## [2026-09-03] update | imu-to-dxl-ref-chip-wiring 名称与说明
- 各器件节增加 **名称** / **说明**（角色、关键约束、LCSC）；NRST 标明 PF2-NRST

## [2026-09-03] update | J1 改为 B3B-EH-A
- XL330 官方座为 JST EH（B3B-EH-A），替换误选的 PH-3A
- Updated: [[imu-to-dxl-ref-schematic]]、[[imu-to-dxl-ref-chip-wiring]]

## [2026-09-03] create | 机身 IMU 参考板 BOM
- Concept: [[imu-to-dxl-ref-bom]] — 按 HD `imu_to_dxl_ref` 终态：必贴 14 + DNP 3；含 LCSC/封装/采购合并
- Updated: [[imu-to-dxl-ref-schematic]]（BOM 摘要→链新页）、[[diy-bom]]、[[index]]
- Index total pages: 48

## [2026-09-04] ingest | JoyandAI/OpenMicroDuck 书签（不并入主 wiki）
- Raw only: `raw/articles/openmicroduck-joyandai-2026-09-04.md`
- Source: https://github.com/JoyandAI/OpenMicroDuck
- 特点：Feetech 舵机路线 + 18650 电池 + 承诺 CERN-OHL-S 硬件开源
- 当前仓库仅 README + LICENSE，无实际硬件/代码
- Updated: `_meta/raw-inventory.md`
- Explicitly **not** merged into entities/concepts/index Layer-2 pages

## [2026-09-04] update | imu-to-dxl 参考板 SCH/PCB/3D 截图入库
- Assets: `wiki/assets/pcb/imu-to-dxl-v0.1-{sch,pcb,3d,3d-top}-2026-09-04.png`
- 丝印：`imu-to-dxl v0.1` · huodianyan · 260904
- J2 改为 **BM05B-SRSS-TB 5P**（含 NRST）；J1 分区示意去掉误写的 PH-3
- Updated: [[imu-to-dxl-ref-pcb-layout]]、[[imu-to-dxl-ref-schematic]]、[[imu-to-dxl-ref-chip-wiring]]、[[imu-to-dxl-ref-bom]]、[[imu-to-dxl-v2]]

## [2026-09-04] create | 头部 IMU 参考板设计
- Concept: [[head-imu-ref-schematic]] — I²C 模块 · 18×14 · LSM6DSV16X · STEMMA QT 4P
- 对照机身 DXL 从机：无 MCU / 无高压 LDO；接 HAT Qwiic；控制环不用
- Index total pages: 49

## [2026-09-04] update | 双 IMU BOM 同步 HD v0.1
- [[imu-to-dxl-ref-bom]]：J2 **BM05B-SRSS-TB** LCSC **C160391**；丝印 v0.1 / 260904
- Concept: [[head-imu-ref-bom]] — 头板采购表（必贴 5 / DNP 2）
- Updated: [[diy-bom]]、[[head-imu-ref-schematic]]、[[imu-to-dxl-ref-schematic]]、[[imu-to-dxl-ref-chip-wiring]]、[[index]]
- Index total pages: 50

## [2026-09-05] ingest | HAT 立创 BOM + 订单 SO26090519869
- Assets: `wiki/assets/procurement/` 两份 XLS（BOM 报价 5 套 + 订单）
- Raw: `raw/articles/lcsc-hat-bom-order-so26090519869-2026-09-05.md`（脱敏摘要）
- Concept: [[elec-hat-lcsc-order-2026-09-05]] — 32 项到货勾选；10 项未订清单
- Updated: [[elec-rpi-robot-hat]]、[[diy-bom]]、[[index]]、`_meta/raw-inventory`
- Index total pages: 51



## [2026-09-05] update | head_imu 转 PCB 摆放示意
- Asset: `assets/pcb/head-imu-placement.svg`
- Updated: [[head-imu-ref-schematic]] §6（含 TP1 小焊盘、C3 近座）

## [2026-09-05] finalize | 三板电子 BOM 定稿
- Concept: [[elec-three-board-bom]] — HAT 锁定 + 机身 AP2210/BM04-4P + 头 I²C 定稿
- CSV: `wiki/assets/bom/three-board-final-bom.csv`
- Body: LDO C176959 · C2=1µ · J2=C160390 · U6=C3040625 · C5=C440198
- Head: 与 HAT 共享 C160390/C1525/C52923/C5267406；上拉 DNP
- Updated: [[diy-bom]] · [[index]] · [[imu-to-dxl-ref-bom]] · [[head-imu-ref-bom]]

## [2026-09-05] ingest | 机身 IMU 立创 BOM + 订单 SO26090520116
- Assets: `imu-to-dxl-ref-BOM-lcsc-20260905.xls` · `lcsc-order-SO26090520116-20260905.xls`
- Raw: `lcsc-imu-to-dxl-bom-order-so26090520116-2026-09-05.md`
- Concept: [[imu-to-dxl-lcsc-order-2026-09-05]] — 立创 11 项勾选；淘宝补 U1/U2（+TP1 匹配可疑）
- Updated: [[imu-to-dxl-ref-bom]]、[[diy-bom]]、[[index]]、`_meta/raw-inventory`
- Index total pages: 53

## [2026-09-05] ingest | 头部 IMU 立创 BOM + 订单 SO26090520046
- Assets: `imu-head-ref-BOM-lcsc-20260905.xls` · `lcsc-order-SO26090520046-20260905.xls`
- Raw: `lcsc-imu-head-bom-order-so26090520046-2026-09-05.md`
- Concept: [[head-imu-lcsc-order-2026-09-05]] — 立创 4 项；U1 C5267406 未订（他渠）；TP1 误配忽略
- Updated: [[head-imu-ref-bom]]、[[diy-bom]]、[[index]]、`_meta/raw-inventory`
- Index total pages: 54

## [2026-09-05] finalize | 双 IMU PCB v0.2 定稿 + 四板合影封面
- Assets: `imu-to-dxl-v0.2-{pcb,3d}-2026-09-05.png` · `imu-head-v0.2-{pcb,3d}-2026-09-05.png`
- 变更：统一 lwimu + 插头规格；机身 LDO/高压线宽；两板 IMU 轴丝印
- Cover: `xhs-four-board-order-2026-09-05.png`（Zero 3W + HAT + 双 IMU · 口号「PCB定稿下单！」）
- Updated: [[imu-to-dxl-ref-pcb-layout]]、[[head-imu-ref-schematic]]、[[dual-imu-board-selection]]、[[index]]

## [2026-09-05] create | 三板 PCB 信息卡（速查）
- Concepts: [[elec-three-boards]]（总入口）· [[board-hat]] · [[board-imu-to-dxl]] · [[board-imu-head]]
- 每卡：规格 / 效果图链接 / 子文档地图 / 缺口清单
- Updated: [[index]]（新分节「三板 PCB」）、[[SCHEMA]] Agent 第一站、[[elec-rpi-robot-hat]]、[[imu-to-dxl-v2]]、[[elec-three-board-bom]]、[[board-interconnect]]、[[dual-imu-board-selection]]、[[imu-to-dxl-ref-pcb-layout]]、[[head-imu-ref-schematic]]
- Index total pages: 58

## [2026-09-05] update | HAT 四视图效果图补齐
- 对照用户四张：正面俯视 / 背面俯视 **已在** wiki（`hat-3d-front` · 旧名 `hat-layout`=背面）
- 新入库：`hat-3d-front-iso-2026-09-05.png` · `hat-3d-back-iso-2026-09-05.png`；别名 `hat-3d-back-2026-09-04.png`
- Updated: [[board-hat]]（§3 四视图表 + 嵌入）

## [2026-09-05] update | HAT / Zero 3W 外形定稿
- HAT：**65×30.9 mm**（6.5×3.09 cm）· 厚 **1.0 mm**
- 主控 [[radxa-zero-3w]]：与 HAT **同板框、同板厚**
- Updated: [[board-hat]]、[[elec-three-boards]]、[[elec-rpi-robot-hat]]、[[radxa-zero-3w]]、[[dual-imu-board-selection]]

## [2026-09-06] create | microduck_imu_to_dxl 固件工程
- 新仓：`microduck_imu_to_dxl/` — STM32G031 + LSM6DSV16X SFLP + DXL 2.0 从机（ID 200 @ addr 124）
- 对齐 `duck-control` 12 B half-quat 契约；半双工 OE#=PA1
- Updated: [[board-imu-to-dxl]]、[[local-workspace-layout]]、[[firmware-flash-matrix]]

## [2026-09-06] review | vs microduck-replica：LSM6 SPI 勘误
- 根因：主 SPI 在脚 **13 SCL / 14 SDA**；脚 **2/3 辅口须 GND**（DS13510）；旧参考图画反
- 另：CS/DE/DATA 上拉、2G241 vs 1G125、双 EH 菊花链等见对照结论
- Updated: [[imu-to-dxl-ref-chip-wiring]]、[[imu-to-dxl-ref-schematic]]


## [2026-09-05] regen | 四板合影封面（准备开工）
- Cover overwritten: `assets/pcb/xhs-four-board-order-2026-09-05.png`
- Refs: wiki CAD/official only (HAT front-iso 新图 + Zero 3W + imu v0.2×2 + Press desk duck); **no** prior AI covers
- Slogan: **准备开工了！** · baoyu / gpt-image-2

## [2026-09-05] pipeline | 四板封面改为切图合成
- `wiki/assets/pcb/composites/`：parts 单板/背景 + `compose_xhs_cover.py`（mm 比例 + 口号叠字）
- Cover: `xhs-four-board-order-2026-09-05.png` · 口号「准备开工了！」
- 单参考生成，避免多图一次整图身份崩坏

## [2026-09-05] cleanup | 移除 AI 生图/合成产物；本仓只存原始资料
- Deleted: `xhs-*` / `*-xhs-*` 封面、`wiki/assets/pcb/composites/`、`.tmp` 生图脚本与 ref 副本
- Scrubbed links: [[board-hat]] · [[board-imu-to-dxl]] · [[board-imu-head]] · [[elec-three-boards]] · [[imu-to-dxl-ref-pcb-layout]] · [[dual-imu-board-selection]]
- Policy: [[SCHEMA]] + [[local-workspace-layout]] — **不做** baoyu/小红书生图；只保留 CAD/官方原始图

## [2026-09-07] reorg | wiki 入 DIY + 四主轴 + temp
- 工作区：`wiki/`、`microduck_imu_to_dxl/`、`image/` → `microduck-diy/`；Press Kit → `wiki/raw/assets/press-kit/`
- 根目录临时物 → `temp/`；根 `README.md` 写清官方/外部/自有
- Wiki Domain/index 改为四主轴；[[local-workspace-layout]] · [[microduck-diy]] 路径更新
- 新建 [[diy-day1-notes]]；Index total pages: **59**
- 并行：`microduck_ros2` 留在工作区根（非本 wiki 主轴）

## [2026-09-06] ingest | microduck 稳定版 Release Source zip
- 下载 12 个 `daemon-v0.2.0`…`v0.10.0` Source code zip → `raw/assets/microduck-releases/`（~76.9 MB）
- 未下 `-dev`/`staging` 预发布（约 17 个）
- Concept: [[microduck-releases]] · 清单含 SHA256
- Index total pages: 57

## [2026-09-06] fix | wiki 审计整改（完整性·SCHEMA·收敛）
- **完整性：** index Total **56**（Concepts 去重 `board-imu-to-dxl`；归档 −1）；[[prior-research-digest-2026-08-30]] 补 `type: query`；OpenMicroDuck `sha256` 补全；补 `assets/pcb/head-imu-placement.svg`；注明 2026-09-01 `dual-imu` 双 create 为历史重复（以首条为准）
- **SCHEMA：** Agent tip 重编号 7/8；目录树加 `assets/`·`_archive/`；标签加 `jlceda` `procurement` `unitree` `final`；「效果图」→ CAD/官方截图；外形口径规则
- **拆分：** [[dual-imu-board-selection]] 压至决策页（~94 行），器件正文指向 ref-*
- **收敛：** 三张立创订单页改为薄指针；机身外形权威 **~25×17**（[[board-imu-to-dxl]]）；MJCF 22×16 仅占位
- **归档：** `concepts/mechanical-bom-alpha` → `_archive/mechanical-bom-alpha`
- **资产说明：** `assets/README.md`；[_meta/raw-inventory] 登记 pcb/procurement/bom

## [2026-09-06] ingest | ROBOTIS XL330 订单 B260905014MP
- Raw: `robotis-xl330-order-b260905014mp-2026-09-05.md`（脱敏：无电话/街道）
- Concept: [[robotis-xl330-order-2026-09-05]] — 15× \$23.90 + DHL \$57.73 = **\$416.23** · Payment complete · ⏳待收
- Updated: [[diy-bom]] §C、[[dynamixel-xl330]]、[[index]]、`_meta/raw-inventory`
- Index total pages: 58

## [2026-09-07] policy | 废弃本地 `txt2cad` 目录
- **不再使用** `D:\projects\txt2cad`（含 `microduck_view*`、`microduck_rl_view`、alpha STEP 试验脚本）
- CAD 工具改为全局 **text-to-cad**；审阅产物落 `temp/cad-review/`；网格真源仍 `microduck_rl/.../robot/microduck/`
- Updated: [[imu-to-dxl-v2]]、[[local-workspace-layout]]；更正本 log 2026-09-01 Viewer 条路径

## [2026-09-07] cleanup | Cursor text-to-cad 0.5 专用
- **删除** `D:\projects\txt2cad`（旧 Codex 旁路工程与 0.4 脚本/产物）
- 技能：Cursor `~/.agents/skills`（cad 等，pin **cadgen 0.5.0**）；运行时：工作区 `.venv-cad`
- **不碰** Codex marketplace/cache；规则改为 Cursor-only
- Updated: [[local-workspace-layout]]、[[imu-to-dxl-v2]]、根 README、`.cursor/rules`

## [2026-09-07] fix | 配件按官方 MJCF 对位装配
- 问题：首版 `casual_outfit` 为示意幽灵块，未与真机网格同帧
- 现：`lib/mjcf_pose.py` + sewn solids + `GLB/fit_check_casual.glb`（头/壳/脚 + 帽包靴同 Location）
- 打开：`http://127.0.0.1:3245/?file=accessories/GLB/fit_check_casual.glb`
- 注：faceted sew 进 cadgen STEP store 会 topology 失败，故审阅用 GLB

## [2026-09-08] ingest | replica 机身 IMU 立创 BOM + 订单 SO2609080348
- Assets: `imu-to-dxl-replica-BOM-lcsc-20260908.xls` · `lcsc-order-SO2609080348-20260908.xls`
- Raw: `lcsc-imu-to-dxl-replica-bom-order-so2609080348-2026-09-08.md`（脱敏）
- Concepts: [[imu-to-dxl-replica-bom]] · [[imu-to-dxl-replica-lcsc-order-2026-09-08]]
- 实付 ¥84.23（13 行）；**STM32/LSM6 未订**；PCB 制板单未附
- Updated: [[diy-bom]]、[[board-imu-to-dxl]]、[[index]]、`_meta/raw-inventory`
- Index total pages: **61**

## [2026-09-08] ingest | replica 机身 IMU 制板 Y38
- Raw: `jlcpcb-imu-to-dxl-replica-y38-2026-09-08.md`（口述：`imu_to_dxl_PCB1_20260908_004528`）
- 规格：双面 · 5 片 · 绿 · 无铅 OSP · 正常 3 天 · 2026-09-08 00:48:07
- Updated: [[imu-to-dxl-replica-lcsc-order-2026-09-08]]、[[imu-to-dxl-replica-bom]]、[[diy-bom]]、[[board-imu-to-dxl]]、`_meta/raw-inventory`

## [2026-09-08] ingest | 淘宝近一月订单 ↔ BOM
- Asset: `taobao-orders-2026-08-09.xlsx`
- Raw: `taobao-diy-orders-2026-08-09.md`（脱敏；链接去 mi_id）
- Concept: [[taobao-diy-procurement-2026-09]]
- 覆盖：HAT 立创 10 缺项；STM32×5 + LSM6×6；轴承 11+3；ZERO 3W；Camera V2 等
- Updated: 各立创订单页、[[diy-bom]]、[[seeed-bearings]]、[[index]]、`_meta/raw-inventory`
- Index total pages: **65**

## [2026-09-08] create | replica 机身 IMU 信息卡 + 完整 BOM
- Concept: [[board-imu-to-dxl-replica]]（独立信息卡）
- [[imu-to-dxl-replica-bom]] 重写为 **16 行+PCB 完整表**（渠道/订单/链接）
- Updated: [[elec-three-boards]]、[[board-imu-to-dxl]]、[[diy-bom]]、[[imu-to-dxl-replica-lcsc-order-2026-09-08]]、[[index]]
- Index total pages: **66**

## [2026-09-08] ingest | OpenMicroDuck + HD-1910 / HL-2909
- Clone: `D:\projects\microduck\OpenMicroDuck` ← [JoyandAI/OpenMicroDuck](https://github.com/JoyandAI/OpenMicroDuck) · HEAD `2c54375`
- Entities: [[openmicroduck]] · [[feetech-hd-1910]] · [[feetech-hl-2909]]
- Updated: [[feetech]]、[[feetech-hl-2915]]（contested vs 规格书）、[[xl330-vs-feetech-servos]]、[[local-workspace-layout]]、raw OpenMicroDuck、根 README、`index`、`raw-inventory`
- Index total pages: **64**

## [2026-09-09] create | Agent 治理薄方案
- Doc: `microduck-diy/docs/agent-governance.md`
- Handoffs: `microduck-diy/handoffs/_TEMPLATE.md`
- Rules: `microduck-pm|hardware|software|train-agent.mdc`；`microduck-ros2-agent.mdc` 改为按需（非 alwaysApply）
- 裁决：train 与 software **不合并**；取消独立 bom 主 agent（电子→hardware，机械→structure，下单→pm）

## [2026-09-09] update | Agent 治理 v0.2
- 名册按已改会话名对齐；补「日常怎么开」与子 agent **免配置**说明
- structure rule 已存在；子 agent 不进名册、不预配置

## [2026-09-09] handoff | 第一张练手 · AI-FanGe 中文改良版评估
- Handoff: `handoffs/2026-09-09-pm-to-pm-aifange-microduck.md`（pm→pm · **done**）
- 裁决：旁路参考、非 diy 主线；正确仓为 `Microduck-build-tutorial`
- Entity: [[aifange-microduck-build-tutorial]]；index 已挂 DIY 节

## [2026-09-09] handoff | AI-FanGe 下游评估 · software + hardware
- open: `2026-09-09-pm-to-software-aifange-sw-eval.md`
- open: `2026-09-09-pm-to-hardware-aifange-hw-eval.md`
- 上游 pm 单已 done；总裁决不变（旁路）

## [2026-09-08] update | DXL 接线示意图（澄清不对称 + 单口 IMU）
- [[board-interconnect]]：删「挂更空的一口」；改为线A=颈头+左腿(10)、线B=右腿+IMU(6)
- 明确：单 3P IMU **可以**且须为链尾/Y叶子；推荐髋旁 Y 分出 ID200
- 附图 ASCII 拓扑

## [2026-09-08] update | 澄清「3P 三通(Y)」非板载端口
- [[board-interconnect]]：Y = 可选一分二线束（并联 GND/VBATT/DATA）；非 HAT 座、非舵机端子
- 默认推荐：普通 3P 线把 IMU 接在线 B 链尾，不必先买三通

## [2026-09-08] update | 机身 IMU 双方案并列 + HD 小板机械定稿
- 用户确认：replica **与** HD 小板均可；HD 继续 **单 3P**；板长≈replica 短边 **22 mm**
- 固定：模型 **电池背板** + 两髋各 1× M2，穿板**两端中部**
- 更新：[[board-imu-to-dxl]]、[[board-interconnect]]、[[elec-three-boards]]、[[dual-imu-board-selection]]、[[board-imu-to-dxl-replica]]、[[diy-bom]]

## [2026-09-08] ingest | LSM6DSV16X 破板照片（安装孔反例）
- Asset: `wiki/assets/pcb/lsm6dsv16x-breakout-ref-one-end-mount-2026-09-08.png`
- 结论：市售破板「两孔同端」易悬臂晃动 → DIY **两孔分两端**，芯片靠跨中
- Updated: [[board-imu-to-dxl]]、`assets/README`

## [2026-09-09] update | 机身 IMU 测试板 1/2 号统一设定
- **1 号大板**：36×22 · 功能完整 · **2× 3P** · **四角**螺丝
- **2 号小板**：22×15 · 功能简化 · **1× 3P** · **两边中心**螺丝
- 重写：[[board-imu-to-dxl]]；更新 [[elec-three-boards]]、[[board-interconnect]]、[[dual-imu-board-selection]]、[[board-imu-to-dxl-replica]]（降为社区对照）、[[diy-bom]]、[[index]]
- 废弃：「replica=现行装机」「HD 长≈replica 宽」等旧表述

## [2026-09-09] update | 1 号大板 32×22 机械 + 布局
- 实测定稿：板框 **32×22**；四角 φ2.2；孔心距边 1.5；长边孔距 **29** · 宽边孔距 **19**
- Asset: `imu-to-dxl-board1-32x22-placement.svg`
- Updated: [[board-imu-to-dxl]]、[[elec-three-boards]]、[[board-interconnect]]、[[dual-imu-board-selection]]、[[diy-bom]]、[[index]]

## [2026-09-09] finalize | imu-to-dxl v0.3 ��Ϣ�� + BOM
- ���������壺**`imu-to-dxl v0.3`** �� 1 �� **32��22** �� ˫ EH �� BM07 �� DXL_BUS/DATA + D2/R6 �� R2�CR5 �� C6
- ��д��[[imu-to-dxl-ref-bom]]������ 24 + DNP 3����� SO26090520116 ��������
- ���£�[[imu-to-dxl-ref-schematic]]��[[imu-to-dxl-ref-pcb-layout]]��[[imu-to-dxl-ref-chip-wiring]]��[[board-imu-to-dxl]]��[[diy-bom]]��[[elec-three-boards]]��[[index]]

## [2026-09-09] finalize | hardware ���� AI-FanGe ��أ���·��
- Handoff: `2026-09-09-pm-to-hardware-aifange-hw-eval` �� **done**
- ���ۣ�OpenRB+Pi Zero+6V+BNO08x �� HAT+imu_to_dxl���ɽ�� EH ������**��**�ư�/����������**δ��** imu-to-dxl v0.3
- Updated: [[aifange-microduck-build-tutorial]]��Ӳ���ӽǣ�
## [2026-09-09] handoff | AI-FanGe · structure mech eval
- sw/hw handoffs: done (pm reviewed)
- open: `handoffs/2026-09-09-pm-to-structure-aifange-mech-eval.md` (links sw/hw siblings)

## [2026-09-09] synthesize | AI-FanGe eval closed (pm)
- Downstream: software / hardware / structure all done
- Verdict unchanged: bypass reference, not diy mainline
- Wiki: [[aifange-microduck-build-tutorial]] + pm handoff section "pm zongping"
- No BOM / imu-to-dxl v0.3 / cad changes


## [2026-09-09] cleanup | Wiki focus on active work (imu-to-dxl v0.3)
- Moved 25 Layer-2 pages to `_archive/` (Feetech/Unitree/OpenMicroDuck/AI-FanGe/replica IMU/head specialty board/JLCEDA research/Day1 notes/digest)
- Rewrote `index.md` (Active first) + `SCHEMA.md` domain/priority
- `_archive/README.md` + `INDEX.md`; raw/ untouched
- Active focus: imu-to-dxl v0.3 BOM/schematic/PCB + interconnect + diy-bom


## [2026-09-09] ingest | imu-to-dxl v0.3 ���� BOM/����
- Assets: `imu-to-dxl-PCB1-BOM-lcsc-BOM260909006112-20260909.xls` �� `lcsc-order-SO26090921960-20260909.xls`
- Raw: `lcsc-imu-to-dxl-v03-bom-order-so26090921960-2026-09-09.md`
- Concept: [[imu-to-dxl-lcsc-order-2026-09-09]]
- **�ж���** ���� `SO26090921960` = diy v0.3 ʵ����ͬ�� BOM �䵥 `BOM260909006112` = **replica ��**���� v0.3 ���Դ��
- ȱ�ڣ�**BM07B J2 δ��**
- Updated: [[imu-to-dxl-ref-bom]]��[[diy-bom]]��[[index]]

## [2026-09-09] correct | v0.3 ���� BOM �䵥��
- �û���������ȷ�䵥 **`BOM260909006316`**��`imu_to_dxl_ref_��_PCB1_1_20260909_194740`��
- Asset: `imu-to-dxl-v03-BOM-lcsc-BOM260909006316-20260909.xls`
- Prior `BOM260909006112` was replica misfile (not v0.3 SoT)
- J2 matched **C160393** (BM07); order `SO26090921960` still missing it
- Updated: [[imu-to-dxl-lcsc-order-2026-09-09]], [[imu-to-dxl-ref-bom]], [[imu-to-dxl-ref-chip-wiring]], [[diy-bom]]

## [2026-09-09] sync | imu-to-dxl v0.3 hardware ? repo/wiki
- Handoff `2026-09-09-pm-to-hardware-imu-to-dxl-v03-sync` ? **done** (unlocks software)
- SoT: `hardware/imu_to_dxl_ref_2026-08-30_18-59-47.eprj2`; pin map: `imu_to_dxl/docs/hardware.md` v0.3
- Path: junction `imu_to_dxl` ? `microduck_imu_to_dxl` (lceda still locks rename)
- firmware/ untouched; USART1 PA11/PA12 documented for software
- Updated: [[board-imu-to-dxl]], [[imu-to-dxl-ref-chip-wiring]], [[imu-to-dxl-ref-schematic]], [[microduck-diy]], [[local-workspace-layout]]
- ��ǰ `BOM260909006112` Ϊ replica �󴫣����� v0.3 Դ
- J2 ����ƥ�� **C160393**��BM07�������� `SO26090921960` ��ȱ����
- Updated: [[imu-to-dxl-lcsc-order-2026-09-09]]��[[imu-to-dxl-ref-bom]]��[[imu-to-dxl-ref-chip-wiring]]��[[diy-bom]]

## [2026-09-10] cleanup | handoffs → workspace root
- Moved `microduck-diy/handoffs/` → `D:\projects\microduck\handoffs/` (local work tickets; not diy repo)
- Updated agent-governance, PM/hardware rules, workspace README; removed diy `.gitignore` handoffs rules


## [2026-09-10] cleanup | microduck-diy 仅留 imu_to_dxl
- Physical rename: `microduck_imu_to_dxl` → `imu_to_dxl` (junction removed)
- Moved out of diy repo: `wiki/` → workspace `wiki/`; `docs/` → `docs/`; `cad/` → `temp/diy-cad/`
- diy main tree: only `imu_to_dxl/` (+ README / .gitignore)
- Updated: agent-governance v0.5, SCHEMA, index, local-workspace-layout, PM/software/structure rules


## [2026-09-10] correct | diy 保留 wiki+cad；docs 在工作区根
- Reverted: `wiki/` · `cad/` back into `microduck-diy/`
- Kept outside diy: `docs/` · `handoffs/`
- diy tree: `imu_to_dxl/` · `wiki/` · `cad/`
- Updated governance §4.2, README, SCHEMA, index, rules


## [2026-09-10] cleanup | wiki 现行页去噪
- Aligned goals with README: official replica + ecosystem + extensions
- Rewrote [[microduck-diy]] · [[diy-milestones]] · [[local-workspace-layout]]
- Trimmed archive/replica/day* noise from index, SCHEMA, diy-bom, board-imu-to-dxl, imu-to-dxl-v2, print-bom-rl
- Social: 精钢葫芦娃 / 人工具身智能


## [2026-09-10] ingest | XL330-CN 国产启动套件台架
- Raw: `xl330-cn-starter-kit-notes-2026-09-10.md`
- Concept: [[xl330-cn-bench-kit]] — U2D2+PHB+电源 + XL330-M288-T-CN；网盘驱动/SDK；B站教程
- Next: user follows tutorials, fills bench checklist
- Updated: [[dynamixel-xl330]] · [[diy-milestones]] · [[index]]


## [2026-09-10] update | XL330-CN 台架通过
- [[xl330-cn-bench-kit]]: **pass**; details TBD (user will supplement)
- Updated: [[diy-milestones]] · [[dynamixel-xl330]] · [[index]]


## [2026-09-10] plan | Zero 3W 主控台架（2G+SD）
- Concept: [[zero3w-bench-plan]] — P0 系统 → P1 IMX219 → P2 接口；HAT/robotd 后置
- Handset: 2G RAM + microSD (vs Press Kit 1G/eMMC)
- Updated: [[diy-milestones]] · [[radxa-zero-3w]] · [[index]]


## [2026-09-10] clarify | P0 镜像重打 vs Etcher
- [[system-flash-armbian]]: microduck 更新 → provision, not reflash Armbian; prefer Armbian Imager; Etcher discouraged
- [[zero3w-bench-plan]] P0 linked


## [2026-09-10] move | seed image → microduck-diy/image
- From `temp/diy-image-seed/` → `microduck-diy/image/`
- Existing: `out/microduck-zero3-20260829-seed.img.xz` (~411 MB); gitignored
- Updated: diy README, [[system-flash-armbian]], [[radxa-zero-3w]], [[zero3w-bench-plan]]

## [2026-09-11] ingest | 飞书 BAM 辨识（祖传 id）
- Raw: `raw/articles/feishu-bam-identification-zuchuanid-2026-09-08.md`
- Concept: [[bam-identification-bench]] — 台架 BOM/注意；XL330 默认可跳过自辨识
- Updated: [[better-actuator-models-bam]] · [[index]] · [[_meta/raw-inventory]]
- Gap: Feishu §5.2 empty; §2–4 image formulas; PDFs not downloaded

## [2026-09-11] governance | v0.6 Issue 主过程面
- Doc: `docs/agent-governance.md` — 废止 handoff 主工单；Issue=`task`/`chore`；handoff=跨域附件
- Updated: handoffs/_TEMPLATE · pm/hw/sw/train/structure rules · SCHEMA · [[local-workspace-layout]] · [[index]]

## [2026-09-11] issue | 台架任务入库 Milestone v0.1
- [#1](https://github.com/ScrapMeta/microduck-diy/issues/1) XL330-CN bench — **closed** (passed)
- [#2](https://github.com/ScrapMeta/microduck-diy/issues/2) Zero 3W P0 system — **open**
- Labels: task/chore/hw/sw/pm/bench/ready-for-pm/wiki
- Updated: [[diy-milestones]] · [[xl330-cn-bench-kit]] · [[zero3w-bench-plan]]

## [2026-09-11] note | 轴承盘切片 XY Hole Compensation
- [[print-bom-rl]] / [[seeed-bearings]]：轴承盘打印 **XY Hole Compensation = 0.05 mm**，保证轴承可套入舵盘

## [2026-09-11] ingest | NP-F550 电池+双充淘宝单
- Source: `Downloads/订单数据 (2).xlsx` → `assets/procurement/taobao-np-f550-order-2026-09-11.xlsx`
- Raw: `raw/articles/taobao-np-f550-order-2026-09-11.md`
- 订单 `3316416782030002460` · 沣标 F550 2200mAh×2 + 标准双充 · ¥90 · 已付款
- 组装计划：拆一充电器充电头 → 装到 `power_support` 作取电触点
- Updated: [[np-f550-battery]] · [[taobao-diy-procurement-2026-09]] · [[diy-bom]]

## [2026-09-15] governance | v0.7 只常驻 pm + 四职能启停
- Doc: `docs/agent-governance.md` · 入口 `AGENTS.md`
- 模型：仅 **pm** 常驻；software / hardware / structure / train 按 Issue 新建→回写→pm 关单→删会话
- ros2 并入 software 范畴（按需 `@microduck-ros2-agent`）
- Updated: pm/sw/hw/structure/train/ros2 rules · handoffs · [[SCHEMA]] · [[index]] · [[diy-milestones]] · [[local-workspace-layout]]

## [2026-09-15] pm | 职能常驻收尾 · 验收关单
- Closed: [#10](https://github.com/ScrapMeta/microduck-diy/issues/10) firmware P0+台架 · [#7](https://github.com/ScrapMeta/microduck-diy/issues/7) zero-reply（由 #10 覆盖）· [#9](https://github.com/ScrapMeta/microduck-diy/issues/9) 机身 DXL 回灌评估（不采用）
- Still open: [#8](https://github.com/ScrapMeta/microduck-diy/issues/8) replica0908 · [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) HAT TTL
- 收尾粘贴稿：`temp/agent-wrapup-prompts-2026-09-15.md`（本地）

## [2026-09-15] governance | v0.8 基础工程 + llm-wiki · 废止 handoff
- Doc: `docs/agent-governance.md` · `AGENTS.md` · 通用模板 G2 `docs/templates/agent-governance-generic.md`
- 启动前提：① 工作区指定 GitHub 基础工程（项目管理）；② 基础工程下 llm-wiki（规格/资料）
- 废止 handoff；跨域写 Issue，结论进 wiki；新开项目填 §9 信息表即可 bootstrap
- Updated: pm/sw/hw/structure/train rules · handoffs/README · [[SCHEMA]] · [[index]] · [[diy-milestones]] · [[local-workspace-layout]]

## [2026-09-15] check | Microduck-build-tutorial 同步复核
- Local `Microduck-build-tutorial` @ `4967821` = `origin/main`（已 fetch）
- Since eval `9a11a40`：删 `microduck/cad/`、`microduck/docs/`、mjlab `robot` 资源；打印改为根目录 `microduck3D打印.3mf`；README 仍误指 `microduck/cad/`
- 裁决维持：旁路非主线；OpenRB/Pi/BNO/6V/ID1–14/51 维契约不变
- Updated: [[aifange-microduck-build-tutorial]] · [[local-workspace-layout]]

## [2026-09-16] clone | ROBOTIS OpenRB-150 板级包（只读参考）
- `OpenRB-150/` ← [ROBOTIS-GIT/OpenRB-150](https://github.com/ROBOTIS-GIT/OpenRB-150) @ `3e2b07e`（2022-07-26）· Apache-2.0 · 230 文件 / 3.5 MB
- 内容：SAMD21 Arduino SAMD 板级支持包（`cores/` `libraries/` `variants/` `boards.txt`；VID `0x2F5D` PID `0x2202`）；含 `usb_to_dynamixel` 示例
- 硬件文件（原理图/Gerber/BOM/3D）不在仓内，走 ROBOTIS 下载 ID 2117/2167/2168/2118·2121
- 用途：AI-FanGe 教程的 DXL 桥参照；**不**进 diy 主线（我们用 HAT TTL）
- Updated: [[local-workspace-layout]]

## [2026-09-16] pm | #4 HAT TTL 复查范围补充
- [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) **仍 open**（主控 ↔ HAT DXL DATA 未打通）；Human 要求 hardware 复查
- 补标签 `hw` · `bench`（原仅 `task`）；pm 注记补 4 项易漏检：DXL 电源使能 / `ttyS2` 占用 / DATA 空闲电平与方向脚 / 单变量原则
- 结论要求：给分支定位（供电·串口·物理层·收发器·软件），附 pin2 电压 + pin3 空闲电平 + ping 波形；标 ready-for-pm 后关单
- 约束重申：7.4 V / 1 A 限流 · 禁止 Type-C 与 +BATT 双灌 · 单挂 U2D2 已验证 XL330 · 本次不用 RS-485
- Open 现行：#4 HAT TTL · #8 replica0908

## [2026-09-16] reconcile | wiki 与 GitHub 脱节修复 + seed 镜像脚本入库
- **问题**：`origin/main` 落后本地 25 改 / 10 未跟踪；[[hat-dxl-bus-debug]] 等流程页**仅存在于本机**，而 #4 正文正指向该页 → 规格真源与远端起点的 agent 脱节
- 修复：`fa66604` 提交并 push 全部 wiki（10 新页 + 25 改页 + BOM/订单表；36 文件 / +1435 −114）· 复核 `origin/main` 已含该 blob
- **入库**：`image/` seed 镜像脚本与 overlay（`build-base-image.sh` · `overlay/` · `microduck-firstboot`）；`image/out/*.img*` 仍 ignore
- `.gitignore`：新增 `res/` · `tmp/`（Dynamixel 工具包、相机 nv12 裸数据、`issue6-handoff.md`）· 收敛为 `image/out/`
- 残留未提交：`cad/microduck_rl_assembly_a1mini.3mf` · `imu_to_dxl_ref_*.eprj2`（非 wiki 范围）
- 教训：职能 agent 回写 wiki 后须**当轮 push**，否则「真源」只在本机生效

## [2026-09-16] triage | 两处挂起二进制改动定案
- `imu_to_dxl_ref_*.eprj2`：**撤销**——SQLite 工程库，仅 `project_structures.ticket` 自增（28120→28166，234 行全 +46），`structure` 设计正文与 `project_uuid`/`branch_uuid` **逐字节一致**；纯 EDA 改写噪声，非设计改动
- 判别方法记入 [[imu-to-dxl-ref-schematic]]（避免下次再查一遍）
- `cad/microduck_rl_assembly_a1mini.3mf`：**真实改动**并提交——对象 138→153（+15）、零件 490→505、新增 `DC15_A01_IDLE_CAP_DUMMY` 等、plate 仍 11；`Metadata/` 新增 plate_2/4 配置
- 工具：`sqlite3` 逐表哈希 + zip 条目对比（本轮把 4 MB 二进制差异定位到单表单列）

## [2026-09-16] governance | v0.11 二进制改动判读 · 版本号去重
- 新增 **§11.1 二进制改动判读**：先看 `git diff --stat` 文件大小 → **变了就直接提交**；大小没变才花几秒定性（zip 条目数 / SQLite 修订计数器）；深挖成本高于收益就先撤销
- 记入已知噪声源：`.eprj2` 打开即自增 `ticket`（`structure` 不变）→ 勿提交
- **版本号去重**：治理版本只保留在细则首行与 log；根 `AGENTS.md` / `README` / pm rule / SCHEMA / index / diy-milestones / 通用模板 一律改为只引用路径
- 起因：一次小改动需同步 7 处版本号，属 v0.9 已批评的「多副本漂移」
- §12 改名「版本与修订」，明示**本文件是唯一版本源**


## [2026-09-16] governance | v0.9 去冗余 · 去歧义 · 清理考古
- Doc: `docs/agent-governance.md` **261→~180 行** · 入口 `AGENTS.md` **43→32 行** · 通用模板 G2→**G3（快照制）**
- **减法**：删 §4.5 合并裁决 / §10 废止迁移 / §11 修订（考古当规范）· 「不用 handoff」25 处 → 1 处 · 布局树 4 副本 → 1（归本 wiki）· 各 rule 只留本职能特有条款（218→**179 行**）
- **补闭环**：wiki 回写**须当轮 push**（A1）· `ready-for-pm` 定为标签且关单时移除（A2）· 标签词表登记（A3）· `assignee-agent:` 入 task 约定（A4）· 同一职能同刻只跑一个会话（A6）· `image/`+`scripts/` 归 software（A7）· 豁免须书面写进 Issue（A9）
- **ros2**：`microduck-ros2-agent.mdc` → **`microduck-ros2.mdc`**，降为 software **附件**（非职能）；技术路线移入 [[ros2-migration-plan]]
- **handoffs/**：9 文件 → 1（去向索引）；`_TEMPLATE.md` 删除
- 工作区 `README.md` 重写为目录导航，布局真源指向本 wiki
- Updated: [[SCHEMA]] · [[index]] · [[local-workspace-layout]] · [[diy-milestones]] · [[ros2-migration-plan]] · [[aifange-microduck-build-tutorial]]

## [2026-09-16] governance | v0.10 治理入仓 · 多仓结构 · 交付物归属
- **结构裁决**：工作区根为**纯目录**（非仓、不承担 PM）——14 个仓中 13 个 origin 属他人；参考克隆重仓不钉版本
- **治理入仓**：`docs/` + 根 `AGENTS.md` → **`governance/`**（新增 §10 工作区形态 · §11 交付物归属）；工作区根 `AGENTS.md` 改**转发存根**
- **否决子模块**：上游无 push 权限 → 改了提交不出去；判据=活跃开发用兄弟仓 / 只读参考用独立克隆
- **新增** `governance/upstreams.lock` + `refresh-upstreams.ps1`：替代子模块钉上游版本（remote/HEAD/Dirty/Behind）
- **清理**：`elec_RPI_Robot_HAT`（gerber/.history/4png/kicad_pro 迁移噪声）与 `microduck-replica`（`.eprj2`/backup）回上游原状；gerber 非唯一副本，官方 `production/PCB01186-C1_*_PCB.zip` 在手
- **建仓**：`microduck_ros2/` 首次入库（78 文件 · `8f0618d`）· colcon build/install/log 排除 · `*.sh` 强制 LF
- 通用模板 G3→**G4**：bootstrap 改为治理入仓 + 转发存根
- Updated: [[SCHEMA]] · [[index]] · [[local-workspace-layout]] · [[diy-milestones]]

## [2026-09-16] pm | #4 本轮定调：先审计方法/脚本/参数
- [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) 追加 pm 注记（[comment](https://github.com/ScrapMeta/microduck-diy/issues/4#issuecomment-5693196184)）：Human 指定本轮**先复查测试方法/脚本/参数**，方法未定案前不动台架
- 预检出 **M1–M6** 待 hardware 逐条裁决（确认/订正/证据不足）：
  - **M1 母线 7.4 V 与 XL330 冲突（最高优先）**：手册 3.7–6.0 V · 实测 7.2 V 即过压红灯闪 · [[body-imu-hat-dxl-power-eval]] 建议 **6.0–6.5 V**；wiki 内 3 处旧值 vs 1 处新值；且 `shutdown=52` **锁存 input-voltage fault 保持 torque off** → **错电压本身能造出「零回包」**，正是本单症状族。J13/J14 针2 直连 `+BATT`、舵机**不过 buck**，故台供电压=舵机电压
  - **M2 限流 1 A 叠 Zero 时不够**：预算 Zero+外设 @5 V ≈1–2 A → 6 V 输入 **1.2–2.5 A**；触限塌陷 → 误判成焊接/overlay 故障
  - **M3 基线缺失**：[[xl330-cn-bench-kit]] 明细仍空（ID/波特率/固件/电压），而本单要求「同一颗已验证舵机」
  - **M4 出厂默认回退未写**：官方 `robotd-design` §2.1——新 XL330 出厂 **ID 1 @ 57 600**，`open_bus` 先 1 Mbps、**再切 57 600** 探测；流程只写 1 Mbps → **假零回包**
  - **M5 无版本化脚本**：`microduck-diy/scripts/` 不存在，SDK/Wizard 在 `res/`·`temp/`（未入库）→ 不可复现
  - **M6 未用官方 `setup-board.sh` 的 `report()`**：已实现 bus 存在/`fuser` 占用 PID/console 冲突（区分 `/proc/cmdline` 与 `armbianEnv.txt`）/failed units；且 `console=display` **重启才生效**易于误判
- 已核对无误：`/dev/ttyS2` · 1 Mbps（官方 `baud_rate=3`）· Protocol 2.0 · getty 须 masked · J13/J14 1=GND/2=+BATT/3=DATA
- 治理改口：§5 software 领地去掉不存在的 `microduck-diy/scripts/`，改为「台架/上机脚本落此、按需新建」
- Open 现行：#4 HAT TTL（先审计方法）· #8 replica0908 · #9 机身取电评估

## [2026-09-16] pm | #4 母线电压定案 6.0–6.5 V
- Human 授权 pm 直接裁决并改口（[ruling](https://github.com/ScrapMeta/microduck-diy/issues/4#issuecomment-5693346059)）；本轮**只做方法审计、不接线上电**
- **母线电压 7.4 V → 6.0–6.5 V**。三条依据：手册 3.7–6.0 V（Max Voltage Limit≈7.0 V）· 实测 7.2 V 即过压红灯闪 · 官方 `shutdown=52` **锁存 input-voltage fault 保持 torque off**（→ 错电压能自己造出「零回包」）
- **限流分段**：纯 HAT **1 A** · 叠 Zero **2–3 A**（Zero 启动峰值超 1 A，触限塌陷会假象成不启动）
- **Key wiring fact**：J13/J14 针2 **就是 `+BATT`**、舵机**不经 buck** → 台供电压 = 舵机电压，无缓冲
- 改口落盘：Issue 正文（Constraints/Acceptance/新增 This round）· [[hat-dxl-bus-debug]] §0/§2/§7 · [[bench-power-supply]]（原「7.4–8.4 V」）· [[hat-solder-kit]] §4.0/§4.3（7.4 V 限定为裸 HAT）· [[bam-identification-bench]]
- 待 hardware：M3 补 #1 基线（ID/波特率/固件）· M4 出厂默认 57 600 回退写进流程 · M5 版本化扫/Ping 脚本 · M6 用官方 `report()` 作一致性基线

## [2026-09-16] pm | #4 关单 · 原症状被推翻
- [#4](https://github.com/ScrapMeta/microduck-diy/issues/4) **closed**（[验收关单](https://github.com/ScrapMeta/microduck-diy/issues/4#issuecomment-5695555482)）；剩余拆到 [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)
- **原症状「主控↔HAT DATA 未打通」不成立**：HAT TTL 本来就通（`/dev/ttyS2` 只读扫描得 ID 1 / model 1200，CRC 通过）
- 真因是**两条方法错误**：①**前提错**——该舵机从未写到 1 Mbps，一直是**出厂 ID 1 @ 57 600**，按原流程只测 1 Mbps 必得**假零回包**；②**脚本 CRC 作用域错**（须覆盖 4 字节 header），且 `self-test` 假舵机**照抄同一错误** → **自检全绿却掩住故障**
- **更正 pm 上一条裁决**：`shutdown=52` **不是锁存**过压——手册 `Shutdown(63)` bit0 = Input Voltage Error，**出厂 53 含 bit0**，而 `robotd` 写的 **52 正好清掉**它；过压只清 `Torque Enable`、**舵机仍应答 Ping/Read**。故「错电压造出零回包」**不成立**，照旧说法会把零回包误归因到电压、漏掉 getty/波特率/物理层。母线 **6.0–6.5 V 结论不变**。教训：pm 当时拿上游**散文**当规格
- 治理：新增 **§3 原则 8「校验要能证伪」**——自检/回环只证两端自洽、不证合规；协议/对外契约/寄存器布局须用**公开向量或独立实现**做锚
- 遗留承重项（→ #11）：**`0x55` 帧异常**——本套件状态帧多一固定字节且 `LEN=len(DATA)+4`，该字节**被舵机自身 CRC 覆盖**（14/14 帧一致）→ 出自固件；须 **U2D2 + Wizard 交叉验证**。另：示波器波形 · 写 ID/波特率到总线值后 1 Mbps 复验 · 限流分段实测
- 交付：`21e2bb8`+`7dad6d5` · [[dxl-bench-method]]（新建）· [[hat-dxl-bus-debug]] · [[bench-power-supply]] · [[dynamixel-xl330]] · [[xl330-cn-bench-kit]] · `scripts/dxl_ping.py`

## [2026-09-16] audit | #4 M1–M6 逐条裁决 · 落 `scripts/dxl_ping.py`
- hardware 方法审计（不接线上电）；手册真源 [XL330-M288 eManual](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/)（当日取）
  - **M1 确认**（母线 6.0–6.5 V）**但机制订正**：手册 `Shutdown(63)` **bit0 = Input Voltage Error**；**出厂默认 53 含 bit0**，官方 `robotd` 写 **52 恰好清掉 bit0** → 旧说法「52 锁存过压」方向是**反的**。且过压只清 `Torque Enable`、红灯持续闪，**舵机仍应答 Ping/Read** → 是「不动」而非「零回包」；旧表述会误导下一任 agent 漏掉真因
  - **M2 确认**（纯 HAT 1 A · 叠 Zero 2–3 A）+ 补「**上电前**按构型设好」（台供恒流触限是**拉低母线**，不是干净断开）
  - **M3 证据不足**：[[xl330-cn-bench-kit]] 基线（端口/ID/波特率/固件/电压）**从未落真源**，wiki·raw·temp·会话均无 → 拒绝臆造，改为**采集位 + 脚本**
  - **M4 确认**：出厂 **ID 1 @ 57 600**（手册 `Baud Rate(8)` 值 1 默认）；官方 1 Mbps → **57 600 回退**顺序写入流程 §1.1
  - **M5 确认**：落 `microduck-diy/scripts/dxl_ping.py`（**只读** Protocol 2.0 · 仅依赖 `pyserial` · 无硬件 `self-test` 通过）+ `scripts/README.md`
  - **M6 确认**：官方 `setup-board.sh` `report()` 作一致性基线，写 §3.1（点名 **`uart2-m0`** · `console=display` **重启才生效** · 区分 `/proc/cmdline` 与 `armbianEnv.txt`）
- Updated: [[hat-dxl-bus-debug]] · [[dxl-bench-method]]（**新建**）· [[bench-power-supply]] · [[dynamixel-xl330]] · [[xl330-cn-bench-kit]] · [[index]] · `.gitattributes`（`*.py` LF）
- **拆页**：[[hat-dxl-bus-debug]] 原 191 行 + 本轮 +79 → 超 SCHEMA 200 行上限；方法/参数/探测顺序/`report()` 基线/验收清单拆至 [[dxl-bench-method]]（199 + 125 行），步骤页只留「照做」的值与指向

## [2026-09-16] governance | v0.12 根即交付仓 · refs/ 收拢参考克隆
- **结构裁决**：工作区根 `D:\projects\microduck` **就是**基础工程工作树（`ScrapMeta/microduck-diy`）——取代 v0.10 的「根为纯目录」
- **理由订正**：v0.10 的「13/14 origin 属他人」回答的是「**能不能提交**它们」，不是「自有仓该放哪」；代价是间接层（转发存根 `AGENTS.md`、治理下沉一级、rule glob 只能写 `**/microduck-diy/**`），且**已实际造成过**「领地写成不存在的路径」这类错误
- **关键动因**：`.cursor/rules/` 那份治理**一直不在版本控制内**——根不是仓就没有历史/备份/review；而复制一份进 `governance/` 会重现 v0.11 刚废掉的「多副本漂移」→ **根即仓是唯一不漂移的解法**
- **迁移手法**：`microduck-diy/` 内容 **+ `.git` 整体上移** → 仓内相对路径不变 → **历史与 wiki 链接自动保留**（迁移后 `git status -uno` 零增删改，`git log` 连续）
- **目录**：13 个他人克隆 → `refs/`（ignore）· `microduck_ros2/` 留根（ignore，但**自有仓、非只读**）· `handoffs/` 移出树 · repo 内 `tmp/` 并入 `temp/`
- **首次入库**：`.cursor/rules/` 6 个 rule（批 1 `618b3f2`）
- 治理改口：§1.1 · §1.3 · §5 领地表 · §8 · §9.1 · §9.3 · **§10 整节重写** · §11 · §12；通用模板 G4→**G5**；`refresh-upstreams.ps1` 扫描目标改 `refs/`
- **新增硬约束 §10.4**：`git clean -x` **会删除被 ignore 的目录** → 一次误操作抹掉 `refs/` 全部克隆 + `temp/`。本仓**只用 `git clean -fd`**；此条**无技术兜底**，靠纪律
- `upstreams.lock` 重生成（15 仓；`(this repo)` 单列）
- 路径口径统一为**从根写**：`governance/…` · `wiki/…` · `refs/<clone>/…`
- **运行发现（待办）**：`refs/microduck_app` **Dirty=1** —— 只读克隆内留有未提交改动，违反 §11；`refs/elec_RPI_Robot_HAT` Behind=1（落后上游 1 提交）

## [2026-09-16] wiki | 路径口径改写（批 3/3）
- **改写规则**：本仓引用去 `microduck-diy/` 前缀（`governance/…` · `cad/…` · `scripts/dxl_ping.py`）；只读参考加 `refs/` 前缀
- **关键判别**：**只引仓库名时不加前缀**（如「官方量产栈是 Rust `microduck/` + MuJoCo `microduck_rl/`」）——`refs/` 只标**本地路径**
- **不改**：GitHub URL 里的 `microduck-diy`（是仓名）· `raw/`（不可变）· `_archive/`（归档）· `log.md` 旧条目（append-only）
- **整页重写**：[[local-workspace-layout]]（布局真源 → 四类目录 + 路径写法约定）
- **新增约定**：`SCHEMA.md` 加「路径写法」四条；`sources:` frontmatter 统一为 **wiki 根相对**（`../refs/<clone>/…`）
- **顺带修正**：`system-flash-armbian` 引用 `microduck/docs/robot/install-dev.md` 补 `refs/`；`zero3w-bench-plan` 样张路径改指 `temp/repo-tmp-2026-09-16/`（原 repo `tmp/` 已并入 `temp/`）
- **既有隐性纠错**：`SCHEMA` 的 `固件 ../imu_to_dxl/` 与 `system-flash-armbian` 的 `[image/](../../image/)` 在旧布局下本就偏一级，现随根即仓而**自然正确**

## [2026-09-16] chore | 迁移后收尾三项
- `microduck_ros2` 建远端 **`ScrapMeta/microduck_ros2`（private）** 并 push（`8f0618d` → `origin/main`）——补上此前挂起的自有仓远端；`upstreams.lock` 的 owned 行现均有 remote
- 移出 `refs/microduck_app` 内后加的 `买的.3mf`（5.3 MB · 未跟踪）→ `temp/from-refs-microduck_app/`；只读克隆恢复 **Dirty=0**（治理 §11：参考克隆内不留改动，stray 文件移出而非改治理）
- `handoffs/` 归档保留在 `temp/handoffs-archived-2026-09-16/`（**未硬删**，唯一副本）
- `upstreams.lock` 重生成：`(this repo)` 与 `refs/microduck_app` 均 **Dirty=0**；`refs/elec_RPI_Robot_HAT` **Behind=1**（落后上游 1 提交——非违规，待定是否更新）
- **仍开放**：参考克隆若为「运行时会自产文件的应用仓」，长期需靠纪律保持 Dirty=0（本次选择移出 stray 文件，未改 §11）

## [2026-09-18] compare | XL330 vs Kpower RD05T（新页）
- **新增 Layer-2**：[[xl330-vs-kpower-rd05t]]（`type: comparison`）· raw ingest `raw/articles/kpower-rd05t-spec-2026-09-18.md` · 原件存档 `raw/assets/kpower-rd05t/`
- **铭牌结论**：RD05T 几乎**逐项等同** XL330-M288-T——尺寸 20×34×26 / 18 g 全同；堵转 6 kgf·cm@6 V(−1.9 %) / 5.2@5 V(−1.9 %)；堵转电流 **1740/1470 mA 完全相同**；空载 125/100 rev·min⁻¹（+1.6 %/−2.9 %）；分辨率 0.088°/pulse ≈ 4096；波特率 9600–4M 同。派生 **Kt 低 2 %**（0.338 vs 0.345 N·m/A @6 V）→ 疑同源电机 + 同档齿轮箱
- **接口确认兼容**：XL330 为 **JST EHR-03**，RD05T 写 `EH2.54-3P` → **同一 EH 系列**；引脚 1 GND/2 VDD/3 DATA 同；电平兼容；**物理层描述逐字相同**（8bit/1stop/No parity）
- **协议未证（第一阻塞）**：规格书只给物理层，**无寄存器地址表**；ID 范围 **0~253** vs XL330「253 ID (0~252)」；自家产品线为 `PWM/UART-TTL/RS-485/CAN-bus`；末尾明写「**控制协议可定制**」
- **缺项**：减速比 · 工作模式 · 内部 PID 增益可写性 · 过压/过流阈值与锁存语义 · 齿轮虚位/回中差/定位精度 · 花键齿数 —— 恰是决定动力学的那些
- **关键推论**：①**过载离合**是 XL330 没有的串联弹性+滑移元件，策略中无此模型；②[[bam-identification-bench]] 硬前提是**可写 P 增益寄存器** → 不可写则**连辨识都做不了**；③XL330 的 `Max Voltage Limit(32)` 默认 **70=7.0 V 且可设**，若 RD05T 卡 6.0 V 不可调，本项目 6.0–6.5 V 母线将**持续过压**
- **判定路径**：最便宜且决定性 = 上台架跑 `scripts/dxl_ping.py info`，看 `Model Number(0)` 是否读回 **1200**（不用猜）
- **分用途**：整机替训练结果 → **不要**；台架/调试备件 → 合适；勿与 XL330 混挂同一受策略驱动总线
- 与既有归档一致：[[xl330-vs-feetech-servos]] · [[xl330-vs-unitree-s288]]（铭牌接近 ≠ drop-in）
- Updated: [[index]] · `comparisons/`（首次使用该目录）

## [2026-09-18] spec | XL330 母线电压天花板 + `Operating Mode(11)` 进基线
- **问题**：`Max Voltage Limit(32)` 默认 70，能否改？本项目 NP-F 满电 **8.4 V** 能否设上去？
- **答案**：**能改，但只能调低**。范围 **31–70 → 3.1–7.0 V**，**8.4 V 设不进去**。该寄存器是**比较器的跳闸点、不是稳压器** → 写 70 只是把报警门槛抬到最高，8.4 V **依然必然置位** Input Voltage Error（+ Alert 0x80），H 桥/母线电容/绕组看到的仍是 8.4 V。**无任何寄存器值能让 8.4 V 合规**
- **项目级发现（重要）**：官方整机 2S 直供**能跑，靠的是 `robotd` 写 `shutdown=52` 清掉 bit0**（= 关掉过压保护），**不是解决了电压**。推论：把 `shutdown` 改回出厂 **53** = 机器人「满电不能用」；台架那颗 CN 舵机**现在就是 53**（2026-09-16 实测）→ 母线超 7.0 V 即 torque off 且锁存，须 REBOOT。同时解释了 2026-09-15 实测：**7.2 V 持续闪灯**（7.2 > 7.0）、6.5 V 正常
- **自我纠正（推翻上一轮的推论）**：先前推断「8.4 V 不多买扭矩，因为 `Current Limit(38)` ≤1750 钉死」——**该推断只在 Current Control(0) / Current-based Position(5) 成立**。手册明确 `Current Limit(38)` 的生效范围**仅这两个模式**；而 XL330 **出厂默认是 3 = Position Control**，此时起作用的是 `PWM Limit(36)`（所有模式），`Current Limit(38)` **不生效** → **升压会让输入电流超出 6.0 V/1.74 A 额定而不受该寄存器保护**，比先前判断**更严重**
- **真源缺口发现**：`Operating Mode(11)` **全仓零记录**（wiki / `raw/` / 脚本都没有）→ 而它恰是判定该问题的前置。**默认 3** 且 `robotd` **不写**该寄存器 → 只能读
- **脚本变更**：`scripts/dxl_ping.py` 的 `REGISTERS` 增加 `operating_mode(11)`；新增 `OPERATING_MODES` / `CURRENT_LIMITED_MODES` 表与 `decode_operating_mode()`，`info` 直接输出「哪个限幅生效」；`self-test` 加 3 条断言（含保留值 2 必须解成 `unknown`）。**自检通过**；用假舵机回放 2026-09-16 出厂基线，`info` 输出逐项吻合
- Updated: [[dynamixel-xl330]]（新 §「母线电压天花板」+ 寄存器表补 4 行）· [[body-imu-hat-dxl-power-eval]] §3.3 · [[xl330-cn-bench-kit]]（新增安全事实 5）· `scripts/README.md`（新 §「为什么 info 也读 `Operating Mode(11)`」）


## [2026-09-18] tool | 换舵机 A/B 工装 `servo_swap_compare.py` + 驱动侧两个缺口（实测确认）
- **背景**：RD05T 厂商称「一比一复刻」「加入很贴合」。但**它的规格书自证不是固件级 1:1**——「过载离合」是 XL330 **没有**的机构，真·1:1 不可能多出一个元件；且 Kt 低 2 %、ID 范围 0~253 vs「253 ID (0~252)」。故「1:1」应读作**外形/接口/装配 1:1**，不是固件/动力学 1:1
- **新工装** `scripts/servo_swap_compare.py`：同一条**确定性激励**分别跑 XL330（基线）与候选件，出**差值之差**报告。刻意**开环**（无策略/MuJoCo/BAM/mjlab）——只依赖 `rustypot`+`numpy`（能在 Zero 本机跑），且**隔离执行器**，避免把执行器差异与控制器稳定性混在一起
- **四相激励**（不同缺陷在不同激励下现形）：`steps_large` 总体动力学 · `steps_small` **死区/回差** · `ramp_slow` 静摩擦 · `reversals_fast` **迟滞**
- **关键指标 `dead_steps`**：**完全没动**（< 指令 20 %）的小步数量。原实现把它折进 `dead_time_s` 的均值，于是一个 3° 死区**被读成「舵机略慢」而不是「有死区」**——正是不可证伪的那种错。改为独立计数后，3° 死区被正确判 **FAIL**
- **诊断分型**（决定能不能修）：只 `tracking_mae` 大 → 摩擦/电机不同 → **重辨识可救**；`dead_time`/`hysteresis`/`dead_steps` 也大 → **机械虚位或柔度元件（离合正是这样）→ 重辨识救不了**，任何控制器都消不掉
- **驱动侧两个缺口（本次实测确认，非推断）**：对 `refs/microduck` 全文检索 `operating_mode` 与 `model_number` —— **零命中**。即 ①全栈**从不设** `Operating Mode(11)`，驱动**依赖默认 3**；`testbench_sim2real.py` 真机路径**显式写** `write_operating_mode(3)`，但**机器人不写**。②`adopt_replacement` **不校验 `Model Number(0)`** → 只要能 Ping + 能写寄存器就被**静默收养**为关节舵机，失败**只会以「走不好」出现**。工装因此**自加** `Model Number != 1200 即拒绝** 的守卫（需 `--allow-unknown-model` 显式绕过）
- **口径订正（本轮发现的工具假阴性）**：本仓 `refs/` 被 gitignore，而 `Grep` 工具默认遵守 `.gitignore` → **对 `refs/` 的搜索会静默返回零命中**。上一条「`Operating Mode(11)` **全仓零记录**」的「全仓」**不成立**，实际只覆盖 wiki/`raw/`/脚本；`refs/` 的结论是本次用 shell 单独检索得到的（结果一致，故**结论不变，措辞过宽**）
- **自检 + 干跑**（两条独立证据）：`self-test` 通过（调度确定性/相位覆盖/与上游 `make_target_schedule` 的 tick 数交叉核对/指标检出/裁决与诊断逻辑）。另用**假舵机端到端**跑通 `record→compare`：伪造一台「同电机但 3° 死区」的件，工装判 **FAIL** 并归因「dead zone…非摩擦」✓
- **干跑抓出两个自身缺陷**（写代码时看不见）：①`dead_steps` 只看**相位内部**变化 → 相位切换处那一步被漏掉；②相位按**均分 tick** 切割 → 短时长把后面相位**截断**。均已修
- **守卫被验证有效（意外收获）**：干跑复用了旧代码留下的调度文件，`record` 依**调度哈希不符即拒绝**返回 5，避免了拿两次不同激励的录音去算「差值之差」
- **未做（Human 本轮只选工装）**：厂商问询信 · 寄存器扫描脚本 · 上游 PR · 开台架 Issue。**`scripts/dxl_ping.py` 仍只读**，本脚本**非只读**（需 `--setup`），已在 `scripts/README.md` 明示
- **边界**：本工装只判**单台执行器**。整机替换另有两道：①**批次一致性**（BAM 是**单台**辨识的，15 台散布大则模型等于错；1~2 台测不出）②策略在环（归 `refs/microduck_rl/scripts/testbench_sim2real.py`，可把其 `--mode sim` 轨迹用 `--sim` 并入本工装）
- Updated: [[xl330-vs-kpower-rd05t]]（§5 新增判定路径第 5 步 · §7 新增开放项）· `scripts/README.md`（新 §「`servo_swap_compare.py`」+ 约定新增「会写总线的脚本须明示非只读」）· [[index]]

## [2026-09-18] bench | 台架物料核实 + 分阶测试决策表 + Wizard 证明力（三处新事实）
- **问题（Human）**：①厂商称可直接上 **DYNAMIXEL Wizard** 且识别成 XL330，能否测？②BAM 对比测试需要台架吗、缺哪些材料（已有小台夹）？③后续还要做 BAM 辨识吗？
- **事实 1：仓里已有整套台架打印件**。`refs/microduck_rl/src/mjlab_microduck/robot/xl330_test_bench/` 下 6 件：`bench_holder` ×1 · `arm` **×2** · `spacer` **×2** · `axis` ×1 · `weight` ×1（+ `xl330` 占位）。装配关系由 `xl330_test_bench.xml` 给出，原始 CAD 是 Onshape（链接在 `config.json` 的 `url`）
  - ⚠ **但这些 STL 不能直接打印**：`config.json` 里 `simplify_stls: true` + `max_stl_size: 1.0`，`arm.stl` 仅 151 KB —— 是**抽稀后**的仿真网格，尺寸/配合精度不足。**要打印须去 Onshape 原文档导出**
  - 关节行程 `range="-1.3962634 1.3962634"` = **±80°**，与 `testbench_sim2real.py` 及 `servo_swap_compare.py` 的 `MAX_ANGLE` **完全一致** ✓
- **事实 2（真源冲突，须修正）**：摆臂质量仓内两处不一致 —— `xl330_test_bench.xml` 写 `mass="0.1"`（注释「100 g payload」），而 `testbench_constants.py` 写 `TESTBENCH_ARM_MASS = 0.12`（**120 g，且 `_set_arm_mass()` 会覆盖 XML**）。差 **20 %**。而 BAM 的硬约束正是「**质量必须实测、禁用铭牌标称**」→ **上机前用 0.1 g 秤称实际臂+配重，按实测值填 `--mass`/`--arm-mass`**
- **事实 3：「能上 Wizard 并识别成 XL330」会发生，但是最弱的证据**。Wizard 按 **`Model Number(0)` 做表查找**：回 1200 → 套 XL330-M288-T 表并如此显示。证明的是**身份声明**，与 `servo_swap_compare.py` 那个「非 1200 即拒绝」的守卫检的是**同一件事**。按证明力分三档记入 §3.1：读（弱）· **写-读回**（中，`robotd` 收养路径前提）· **写 P 增益并看阶跃响应是否真变**（强，BAM 电气前提）。**只读不算证明**：固件可以「存值不用」
  - **陷阱**：Wizard 套的是 **XL330 的表含合法范围/单位**；克隆件某地址实际含义不同时 **Wizard 照 XL330 显示、看不出差别** —— 即本 wiki 已记过的那类「合理但错误」的数（`model=45056`、`max_voltage_limit=1792.0 V`）。**工具本身掩盖差异**，故「Wizard 正常」不可当通过
  - **Wizard 顺带能定论 `0x55` 帧异常**（长期待办）：它是**独立实现**，可判固件怪癖 vs 脚本问题
- **分阶测试（新）**：T1 身份（无台架）→ **T2 空载 A/B（无台架，~1 小时）** → T3 负载 A/B（~1 天）→ T4 辨识（数天–数周）。**关键理由**：`dead_steps`/`hysteresis`/`dead_time` 测**虚位与柔度**，**空载即显形**（间隙内自由行程不需外力）；只有 `ramp_slow` 摩擦对比需配重，**空载无力矩则静摩擦不被激励** → **空载的 `tracking_mae` 不可判摩擦，只判虚位**
- **「要不要做 T4 辨识」= 取决于 T2/T3 的**诊断分型**，不取决于「能不能用」**：虚位/迟滞型差异 → **不必做**（BAM 拟的是**摩擦**：库仑+黏滞+负载相关，**表达不了运动学/结构属性** → 白费）；仅 `tracking_mae` 大且虚位正常 → **值得做**。**顺序：先 A/B（1 天）再决定辨识（数天–数周），别反过来**
- **两道未覆盖**：①**批次一致性**（BAM 是**单台**辨识；15 台散布大则模型错，**1~2 台测不出**）②**策略在环**（归 `testbench_sim2real.py`）
- Updated: [[bam-identification-bench]]（BOM 增「打印件」+「质量真源冲突」+ 新 §「分阶测试」；结论表「何时值得搭辨识台」补指向）· [[xl330-vs-kpower-rd05t]]（新 §3.1 Wizard 证明力三档 + §3.2 可即刻回答的两件事 + §3.3；§5 判定路径重排为 1/2/**2b**/3/4/**5a**/**5b**/6 并加「先便宜后贵」顺序原则）· `scripts/README.md`（新 §「先空载跑，别等台架」）

## [2026-09-18] query | RD05T 厂商询问函（新页 `queries/`）+ 寄存器地址逐项核对
- **新增** `wiki/queries/rd05t-vendor-inquiry-2026-09-18.md`（`type: query`）——`queries/` 目录首次启用（原唯一一页已在 `_archive/`）
- **结构**（便于厂商逐条答、便于事后追踪）：**使用条件**（先给对方判断依据，不必反问）→ **A 三个决定性问题** → B 寄存器对照 → C 保护阈值 → D 机械/动力学 → E 供货一致性 → 「需要/不需要什么」
- **A 三个决定性问题**（任一不满足即淘汰）：`A1` 是否完整实现 Protocol 2.0 · `A2` `Model Number(0)` 与 `Firmware Version(6)` **具体数值**（「能识别成 XL330」不足以回答）· **`A3` `Position P Gain(84)` 是否可写且写入后响应真的改变**（分①生效 / ②读回是新值但响应不变 / ③被忽略三档，请其实测；②③ 则 BAM 路径直接不可用）
- **准确性核对（重要）**：本地无权威控制表（`refs/` 里没有地址表），故去 **XL330-M288 eManual** 逐项核对信中全部地址与范围 —— **全部一致**：`Model Number`0 · `Baud Rate`8 · `Return Delay Time`9（默认 250 = 500 µs/台 ✓）· `Operating Mode`11 · `Max/Min Voltage Limit`32/34（31~70 = 3.1~7.0 V ✓）· `PWM Limit`36 · `Current Limit`38 · `PWM Slope`62 · `Shutdown`63（默认 53 ✓）· `Torque Enable`64 · `Status Return Level`68 · `Hardware Error Status`70 · `Position D/I/P Gain` **80/82/84**（范围 **0~16,383**，P 默认 **400** ✓）· `Goal Position`116 · `Present PWM/Current/Velocity/Position` **124/126/128/132**（**124–135 无空隙** ✓）· `Present Input Voltage/Temperature` **144/146**（**144–146** ✓）。信中表格已补上 **XL330 默认值 + 范围** 两列，使厂商可按行答「是/否」
- **核对中发现一条此前未记录的规则（已补入对比页 §4.2）**：eManual 明确 —— **切换 `Operating Mode(11)` 会重置增益**（`Position PID(80,82,84)`、`Velocity PI(76,78)`、Feedforward(88,90)）。→ **写入顺序必须先设模式、再设增益**；若克隆件重置规则不同，**同一条命令序列会得到不同的最终增益，而读回值可能都「对」**（又一类「合理但错误」）。与本项目相关：`robotd` **从不设** `Operating Mode`，而 `testbench_sim2real.py` 真机路径是「先 mode 再 gain」——**顺序是对的**
- **信中新增 B5**：问厂商是否同样遵循「EEPROM 区仅在 `Torque Enable(64)=0` 时可写」与「切模式重置增益」两条规则（我们依赖前者写 EEPROM、依赖后者定写入顺序）
- Updated: [[index]]（「主线执行器/采购」下新增一行）· [[xl330-vs-kpower-rd05t]]（§5 第 1 步加询问函链接 · §7 开放项标注「询问函已备（**待发出**）」· §4.2 新增「增益会被 Operating Mode 重置」一行）· `log.md`

## [2026-09-18] query | A3 依据升级：BAM 源码本身就在写 P 增益寄存器
- **由来**：一条后台搜索（找 `refs/` 里 SDK 头文件中的 DXL 地址常量）完成。结论：**`refs/` 无 DXL SDK 地址表**，只有对 rustypot 封装函数的调用（地址在编译好的 `.pyd` 内）→ **当日改用 XL330-M288 eManual 核对是唯一可行路径**，前述核对结论不变
- **顺带捞到的佐证（有价值）**：**BAM 官方辨识脚本自己就写该寄存器** —— `refs/microduck_rl/.venv/.../bam/dynamixel/record.py:65`，在辨识 setup 循环里**每轮**调用 `write_position_p_gain(ID, args.kp)`（`Xl330PyController`，1 Mbps，timeout 0.01）。本项目 `refs/microduck_rl/scripts/testbench_sim2real.py:317` 同样先写、`:322` 再读回校验
- **意义**：询问函 **A3**（`Position P Gain(84)` 可写且生效）的依据，从「[[bam-identification-bench]] 社区 BOM 笔记的转述」**升级为「BAM 源码行为」** —— P 增益不可写 = **辨识工具直接跑不起来**，不是我们额外加的要求。对厂商的说服力不同（是上游工具链的硬需求，不是我方偏好）
- **信中增强**：A3 补「该方法的官方实现本身就要求改写此寄存器」说明；并追加一问「**读回值是否等于写入值**」——固件静默钳位超范围值是常见做法，钳位则要求给出实际接受范围
- Updated: [[xl330-vs-kpower-rd05t]] §4.5（补源码出处，注明「该前提不是社区笔记的转述」）· [[rd05t-vendor-inquiry-2026-09-18]]（A3 依据 + 读回校验一问）· `log.md`

## [2026-09-18] query | 询问函补齐 `Protocol Type(13)`：A1 的直接验证项此前漏在表外
- **由来**：第二条后台搜索完成（在 `refs/` 找 P Gain 地址字面量 + 导出 `wiki/entities/dynamixel-xl330.md` 的地址表）。结论：**`refs/` 无地址常量，只有注释**；wiki entity 页确有完整地址表 —— **均无新信息**
- **但暴露一处真缺口**：**A1 问「是否完整实现 Protocol 2.0」，而表中没有 `Protocol Type(13)`** —— 它恰恰是该问题的**直接验证项**。核准 eManual：`Protocol Type` = **RW，默认 2，范围 2 ~ 22**（`Drive Mode`=10 默认 0；`Homing Offset`=20；`Max/Min Position Limit`=48/52 默认 4,095/0；`Feedforward 1st/2nd`=90/88）
- **信中补齐**（A1 与 B1）：A1 补「最直接答法：读回 `Protocol Type(13)` 数值」；B1 表新增 **`Protocol Type(13)`**（标为 A1 直接验证项）· `Drive Mode(10)` · `Homing Offset(20)` · `Max/Min Position Limit(48/52)` · `Feedforward 1st/2nd(90/88)`；并把 `Goal Position(116)` 的「范围」由「4 字节」订正为 **`Min(52)` ~ `Max(48)`**
- **新增 B6（静默裁剪）**：XL330 的 `Goal Position(116)` 可写范围受 `Min/Max Position Limit(48/52)` 约束（出厂 0~4,095 = 一整圈）。问：出厂值与可写范围？超限时**裁剪**还是**拒绝**？我们的 ±80°（≈±910 pulse）是否落在限位外？
  - **为何单列一问**：**被静默裁剪的指令看起来完全正常** —— 舵机照常动、只是动得不够，**反馈里读不出「指令被改过」** → 会伪装成「舵机没劲」或「模型不准」，极难定位。与本项目已记录的「合理但错误」（`model=45056`、`max_voltage_limit=1792.0 V`、被钳位的增益）**同属一类**
- Updated: [[rd05t-vendor-inquiry-2026-09-18]]（A1 · B1 表 5 行 · 新增 B6）· `log.md`

## [2026-09-18] docs | 问询函出 PDF（新工具 `md_to_pdf.py`）+ 交付前审计订正 5 处
- **由来**（Human）：md 文件没法看，检查一下准确性，输出成 pdf
- **审计订正**（均为上几轮插行/命名留下的，逐项对 eManual 重核后改）：
  1. **B1 表地址乱序** — `Max/Min Voltage Limit(32/34)` 被插在 `Position Limit(48/52)` **之后**（补行时插错位置）。已按地址重排为 0·6·7·8·9·10·11·13·20·32·34·36·38·48/52·62·63·64·68·70·80·82·84·88/90·116·124..135·144..146
  2. **表漏 `ID(7)`**（默认 1，范围 **0 ~ 252**）—— 而驱动**会写它**（`adopt_replacement` 要把出厂 ID 改成关节 ID）。同时它**正是**对比页记的那处出入（贵司规格书写 ID **0 ~ 253**，而 DXL 2.0 规定 253 为保留值）→ 故**新增 B7**，追问实际范围与写入后是否需重启生效
  3. **表漏 `Firmware Version(6)`** —— A2 问了它却没进表。地址经 **eManual 与 `scripts/dxl_ping.py` 的 `(6, 1, "1")` 双向确认**
  4. `Feedforward 1st / 2nd Gain | 90 / 88` 地址**降序**，易被读成笔误 → 改为 `Feedforward 2nd / 1st Gain | 88 / 90`（升序，标签与地址顺序一致）
  5. **标题名不副实**：「（寄存器兼容性）」但信中还有保护阈值 / 机械动力学 / 供货一致性 → 改为「**RD05T 兼容性问询函**」
- **新工具 `scripts/md_to_pdf.py`**（markdown → HTML → 无头 Chrome 打印）。刻意**不做静态站点生成器**：只渲染一页，剥掉 frontmatter / `[[wikilink]]` / 点名要删的尾行，而**不是**让人再维护一份「可发送副本」——**第二份副本就是会漂移的那份**
- **验证（不只信退出码）**：嵌入字体 `MicrosoftYaHei` + `Consolas` **全为 ttf 子集**（→ 「中文渲染成方框」的硬否证，该故障**不体现在退出码里**）· 页眉页脚**无 URL / 路径残留** · 5 页 **4545 字符**可提取 · 关键行（`Protocol Type`·`2 ~ 22`·`Position P Gain`·`0 ~ 16,383`·`0.229`·`1,200`·`静默裁剪`）**全部命中**；两处初次「MISS」经复核**只是窄列内换行**（`Return\nDelay Time`），非内容缺失
- **坑（值得记）**：Chrome 对**相对 Windows 路径**会报 `cannot find the path specified` 却**仍返回 0 且不产文件** → 工具改传**绝对 / 正斜杠**路径，并以「文件真的在 + 文字能读回」判成功
- 附带：`scripts/README.md` 约定加**唯一豁免**（非台架工具以 `--check` 声明前置条件，无 `self-test`）；PDF 与源 `.md` **同级**存放，是**派生物**，源改须重生成
- Updated: [[rd05t-vendor-inquiry-2026-09-18]]（B1 重排 + `ID(7)` + `Firmware Version(6)` · 新增 B7 · 标题）· 同目录新增 `.pdf`（可发送件）· `scripts/md_to_pdf.py`（新）· `scripts/README.md` · [[index]] · `log.md`

## [2026-09-18] power | 母线运行点定案 6.0 V（6.5 V 降级为台架值）；RD05T 过压风险随之降级
- **由来（Human）**：电压为 5v·6v，会用降压模块到 6v，保持 6v 运行；之前的 6.5v 是测试环境
- **定案**：整机母线 = **6.0 V**（电池 → 降压模块 → 6.0 V，**长期运行**）。6.0 V 是 XL330 手册工作区 **3.7–6.0 V 的上限**（推荐 5.0 V）；取上限换扭矩（**0.60 vs 0.52 N·m，+15 %**；123 vs 103 rev/min），代价是**对模块超调无余量**。**6.5 V 降级为「台架曾用值」**
- **两处连带结论（比订正本身重要）**：
  1. **问询函 C 节的前提被推翻** —— 原写「我们的工作电压**高于**标称值，此项风险最高」，**已不成立**。运行点**等于**标称上限，故 C 的问题从「会不会超压」改为「**跳闸点相对 6.0 V 还剩多少余量**」（XL330 的 `Max Voltage Limit(32)` 出厂 70 = 7.0 V，即留 **1.0 V**）。并新增一问：**毫秒级过压尖峰耐受**（多台同时制动回灌）+ 母线电容建议
  2. **RD05T 对比的头号风险降级** —— §4.3 原「若 RD05T 过压阈值卡在标称 6.0 V 且不可调 → 6.5 V 持续过压、机器人瘫」是**风险最高的「直接跑不起来」项**。母线定案 6.0 V 后该场景**不再存在**（两侧运行点都在各自标称上限）→ 残余风险从「系统性过压」降为「**余量**」（模块超调 / 回灌致误跳）
- **新增约束（辨识）**：**辨识 vin 必须 = 6.0 V（运行点）**。辨识出的模型**对应辨识时的供压**（供压决定可用扭矩与电流爬升：6.0 → 0.60 N·m，6.5 线性外推约 0.65，差 ~8 %）→ 用 6.5 V 辨识 = 模型对应另一电压点，装到 6.0 V 的整机上等于换了执行器。已写入 [[bam-identification-bench]] 与 [[dxl-bench-method]]
- **口径分工（台架带保留）**：**6.0–6.5 V 仍是调试可用带**（写 ID / 波特率 / 打通总线等与精确电压无关）；**只有动力学标定须锁 6.0 V**。故 bench 页**未改带、只加锁**
- Updated: [[rd05t-vendor-inquiry-2026-09-18]]（使用条件表 → 6.0 V + 「关于 6.0 V」说明 + C 节改问「余量」+ 新增瞬态耐受问）→ **PDF 已重生成**（5 页 · 4962 字符）· [[xl330-vs-kpower-rd05t]]（§1 电压行标「运行点＝双方上限」· 结论新增第 5 条 · §4.3 过压行降级 · §5 第 3 步改为量余量）· [[dynamixel-xl330]]（项目内用法）· [[body-imu-hat-dxl-power-eval]]（§3.1 表 · §3.3 · §5 裁决）· [[bench-power-supply]] · [[dxl-bench-method]] · [[bam-identification-bench]] · `log.md`

## [2026-09-19] bom | 原厂「喇叭 / 激光雷达」查型号与尺寸 —— 两条订正
- **由来（Human）**：查一下原厂 bom 的喇叭和激光雷达什么型号的尺寸
- **订正 1：「激光雷达」不是激光雷达，是 ST 的 8×8 多区 ToF。** 原厂 Press Kit 写 *compact LiDAR*，逆向结果是 **VL53L8CX / VL53L5CX（DToF，非扫描式）**。**选型/询价不能按 LiDAR 去找**（会拿到机械旋转/固态扫描，价格与接口都不是一档）。[[vl53-tof]] 页标题去「LiDAR」并加警示
- **订正 2：喇叭原厂 BOM 无型号，但 CAD 留了矩形净空 35 × 25 × 7 mm。** `speaker.stl` 是**长方体占位体**（12 三角形 / 0.7 KB）。**原 wiki 写「直径 28–40 mm 圆形」不够准** —— CAD 留的是**矩形**包络，圆/矩都可能，须按 35×25×7 挑或实测出声孔
- **尺度可信性核对（重要）**：同一脚本算出 `elec_rpi_robot_hat_pcb.stl` = **65.0 × 30.0 mm**，与真实 HAT 尺寸吻合 → 证明网格为**米制真实尺度**，故 35×25×7 可用
- **在役器材实况（采购关键，源码注释给出）**：`tof/src/sensor.rs:76` 原文 —— revision `0x02`(L5CX) 是 *"the older sensor, and **the one most ducks in the field have**"* → **在役机器多数装 L5CX**，L8CX 是更新一代。固件**两代都自动识别**（`0x0C`/`0x02`）
- **地址语义查清**（`tof/src/main.rs:102-107`）：`0x29` 两代出厂默认；`0x52` 是原型期为避让一颗要 `0x29` 的 I²C IMU 而改的 —— **该 IMU 已移除，但改过地址的传感器掉电不丢**，故两地址都要试
- **头壳出声孔：查不出可靠结论**（已如实标注，不猜）。`hole_analysis.json` 里 `bottom_head_shell` 16 孔 / `top_head_shell` 6 孔 / `face_part` 18 孔，**均无 35 mm 级孔** —— 最大是 `bottom_head_shell` 上两个 **Ø13.5 × 1.2 mm** 浅孔。可能是栅格由许多小孔组成被逐孔检出，或逆向网格简化掉了栅格。**须看实物**。Human 本轮选择自行实测（不继续挖）
- **仍缺的尺寸**：ToF **breakout 模块**外形 —— 原厂用模块（否则接不出 Stemma 4P）但**BOM 未钉型号**，故无权威值；裸芯片为 **6.4 × 3.0 × 1.75 mm**（⚠️ 来自 ST 数据手册，**仓库内无此数据**，已标注来源）
- Updated: [[vl53-tof]]（全面重写：型号/在役实况/光学/接口/地址语义/尺寸两级 + 采购坑）· [[hat-solder-kit]] §6.3（喇叭净空 35×25×7 + 尺度核对 + 出声孔存疑）· `log.md`

## [2026-09-19] governance | 查 refs 上游更新：5 个落后；`upstreams.lock` 的 `Behind` 一直在骗人
- **由来（Human）**：查看 refs 工程是否有更新
- **方法先纠自己的错**：`refresh-upstreams.ps1` **从不 fetch**，其 `Behind` 只比 `origin/<branch>`（**上次 fetch 的快照**）与 HEAD —— 直接跑它等于**拿 18 天前的读数问今天**。故先对 13 个克隆逐个 `git fetch`
- **结果：5 个落后，全部可快进（`ahead=0`），`Dirty` 全 0**（无 §11 违规）
  - `refs/microduck` **111** 提交 / 111 文件（**0.12.0 → 0.14.1**）
  - `refs/microduck_rl` 计数 **1177**（⚠️**虚高**，见下）· `refs/OpenMicroDuck` 17 · `refs/microduck-replica` 9 · `refs/elec_RPI_Robot_HAT` 1
  - 无更新 8 个：`microduck_app` · `microduck_kinematics_rs` · `microduck_maploc_rs` · `microduck_pet_detect` · `microduck_sounds` · `Microduck-build-tutorial` · `microduck-simulator` · `OpenRB-150`
- **⚠️ 1177 是计数假象，不等于 1177 个提交的工作量**：`rev-list` 把 **merge 带进来的旧历史**也算进 `HEAD..origin/develop`（committer date 回溯到 **2025-12-06**），而 `git diff` 只有 **12 文件 +2598/−32**（VelStand 环境重构 · `robotallcollisions_backlash.xml` · `distill` 任务 · odom anchor 脚本）。**教训：`Behind` 只用来决定「要不要看」；「变了多少」必须看 `git diff --stat`**
- **逐项核对 wiki 引用：零处失效**（上游动了，但没动我们引用的那些）—— `duck-control`（`adopt_replacement` 无 Model Number 守卫）**未改** · `tof/src/sensor.rs`/`main.rs` **未改** · `configd/src/pad.rs` **未改** · `testbench_constants.py`（`TESTBENCH_ARM_MASS=0.12` 与 XML 0.1 的冲突）**未改** → **问询函 / ToF / 喇叭 / 手柄四页均不需返工**
  - `padd/src/main.rs` 改了，但只是**双柄修复**（只允许第一只柄的事件生效 —— 防另一只手柄的 Start 开动别人的机器）→ **按键表不变**
  - `robotd/src/main.rs` 改了，只新增 `sitting` 状态；`cheatsheet.md` 新增相机监视块 → 均为增量
- **工具缺陷（本节核心，已修）**：`upstreams.lock` 的 `Behind` 列**只反映上次 fetch**，而脚本**自己不 fetch**。证据：`origin` 的 reflog **最后一条就是 clone 那一刻（2026-08-29）** → 故 09-16 生成的 lock 报 `microduck Behind=0`，实际早已落后；**唯一非零**的 `elec_RPI_Robot_HAT Behind=1` 只是**恰好被单独 fetch 过**。**这个 lock 会给人「一切都最新」的假安心，与它锁定版本的用途相悖** → 加 `-Fetch` 开关（**默认仍不联网**，脚本保持只读 + 瞬时）· 表头新增 **`Remote state`** 行自述本次是否联网 · Checks 增一条「**未经 `-Fetch` 的 `Behind=0` 不构成「已最新」的证据**」
- **顺带发现的升级机会（待办，未做）**：`microduck-replica` 那 9 个提交与我们直接相关 —— ①**整机 15 颗舵机首次上电、能站起来坐下**（附 `首次上电-2026-09-18.mp4` · `站起来.gif`）②`software/飞特适配架构.md`（493 行）与 **`docs/飞特资料/`（飞特官方一手：SCS 协议 · SMS/STS 磁编码内存表手册）** ③`tools/servo-web/`（网页舵机调试台 + `feetech.py`）④`imu_to_dxl 首板实测：3.3 V 正常，J4/J5 PH 座外壳跟飞特插头不配（削壳能用，v2 换座）`（与本项目 imu_to_dxl 同类工作）⑤`tools/radxa/` 烧卡脚本。其中**飞特官方内存表**可把 [[xl330-vs-feetech-servos]] 的依据从社区转述**升为厂商一手**
- **执行**：`-ff-only` 快进 5 个克隆（`microduck 6507d2e→344925c` · `microduck_rl 53b8971b→cb70b792` · `microduck-replica f533679→3599731` · `OpenMicroDuck 3992277→21c5a19` · `elec_RPI_Robot_HAT 23eab11→88d51fa`），全部 `Dirty=0`
- Updated: [[local-workspace-layout]]（版本锁定行加 `-Fetch` 与「`Behind=0` 不等于已最新」）· `governance/agent-governance.md` **§10.3 重写**（补「脚本默认不联网」+ 上述判据）· `governance/upstreams.lock`（两次重生成）· `governance/refresh-upstreams.ps1`（`-Fetch` + 表头 + Checks）· `log.md`

## [2026-09-19] servo | 挖 microduck-replica 的飞特路线：SCS 是 DXL 1.0 血统；并订正本 wiki 4 处错值
- **由来（Human）**：研究一下 microduck-replica 的飞特舵机，参数指标和官方、kpower 的比较一下，协议、sdk、实现、硬件等挖掘一下
- **结论先行**：这条路换的不是「同一颗舵机的另一家供应商」，而是**换了一个动力学等级**。HD-1910 在 6 V 堵转 **1.18 N·m / Kt 0.735 N·m/A**，XL330 是 **0.60 / 0.345**——**Kt 2.13 倍**；而 RD05T 的 Kt 与 XL330 只差 **2 %**。所以 **RD05T 理论上能复用原厂训练结果，HD-1910 不能**（replica 自己写明「大概率不能直接走」）
- **协议（最有价值的发现）**：**飞特 SCS = Dynamixel Protocol 1.0 血统**，不是 2.0 ——
  - 帧格式**逐字相同**：`FF FF ID LEN INSTR …PARAMS CHK`，`CHK = ~(ID+LEN+INSTR+ΣPARAMS) & 0xFF`（1.0 的取反和，**不是 2.0 的 CRC-16**）
  - 指令码大面积同源：PING/READ/WRITE/REG_WRITE/ACTION = 1/2/3/4/5；**REBOOT = 0x08 同码同义**；SYNC_READ/WRITE = 0x82/0x83
  - **但寄存器表无一处运动核心同址**：ID 5 vs 7 · 模式 33 vs 11 · 目标位置 42 vs 116 · 当前位置 56 vs 132 · 增益 **21/23/22 在 EEPROM** vs 84/82/80 在 RAM · 扭矩开关 40 vs 64。仅温度上限(13) 与锁(55) 同址
  - ⚠️ `0x06` 是「**恢复 0x09 备份的参数**」，**不是恢复出厂** —— 依据 2019 版手册或 SDK 头文件会得出「飞特没有 REBOOT」的错误结论（replica 与两轮评审都栽过）
- **一个会伪装成「舵机没劲」的坑**：飞特位置/速度/电流用 **BIT15 方向位（符号-幅值）**、负载用 BIT10；DXL 用**补码**。`0x8001` 实为 −1，按补码解码是 **−32767**，**差 3 万倍且不报错**。位置寄存器在舵机模式只用 0–4095，两编码恰好一致 → **「位置读对了」不能证明解码对了**，属本项目反复遇到的「合理但错误」类
- **实现（两个设计层面的收获）**：
  1. **增益在 EEPROM，但「锁着写」正好当 RAM 用** —— 内存表 55 原文「写 1 打开写入锁，写入 EPROM 地址的值**掉电不保存**」→ 不解锁直接写 P = 写入被接受、只是不落盘 = XL330 的 RAM 语义，**零磨损**。把一个硬件限制反用成特性。附带：**D 不要清零**（出厂 D=32 是 320:1 高减速比的整定）
  2. **换协议最容易被忽略的连带代价：IMU 不在总线上了** —— 官方把 `imu_to_dxl` 做成 DXL 从机（ID 200）混在同一次 `sync_read` 里，**协议一换这个设计就断**。处置：A 重写小板固件冒充飞特 ID 200 / B BNO085 直飞 I2C（先做 B）
  - 另两条：出厂模式是 **4**（不是 0/3，且两个官方来源对模式 4 含义不一致 → 以实机底账为准）· **应答级别必须 = 1**（`0` 时除读/PING 不回包，rustypot 每笔写超时 30 ms，15 颗拖垮 init）
- **SDK**：飞特官方只有 C/C++、Python、FD 上位机（**全在 Gitee，无 Rust**）；但官方 `duck-control` 已依赖的 **`rustypot 1.6.0` 就带飞特 STS 内存表**（据 replica：`v1.rs` 的 `0x82/0x83` 就是**为飞特加的**，DXL 1.0 本身没有）。⚠️ **rustypot 未在本工作区安装/vendored，此条我方尚未独立复核**
- **硬件（三处会咬人）**：① **脚序是反的**——HD-1910 `1=Signal 2=Vcc 3=GND` vs XL330/RD05T `1=GND 2=Vdd 3=Data`；好在 **2.0 vs 2.5 mm 间距插不进对方**，只剩「自己压线压反」这一种可能 ② **外形：三台同尺寸**——**20×34×26（含主舵盘）**；规格书的 **23 mm 是「不含主舵盘」的量法**，不是深度差 ③ **供电哲学相反**——HD-1910 原生 4–8.4 V（2S 正当），官方 XL330 却是**超压跑**（上限 6.0 V 挂 6.6–8.2 V，靠 `shutdown=52` 清掉过压位）
- **⚠️ 我在此处犯过一个错，Human 当场纠正**：初稿把 HD-1910 写成「薄 3 mm → 结构上不是直接替换」，**把「不含舵盘的量法」当成了真实差异，还顺着它推了一个不存在的原因**。而**我们自己的来源早就标注过**——[[openmicroduck]] 的 `docs/servo.md` 原文：「飞特 / ED330 是 34×20×23、深度少约 3 mm，**但HD1910来说，其实是测量部位不一样**，孔距要拿实物核」。**教训：一手规格书的尺寸要问清量法与基准**（含不含舵盘/花键/线座），否则会拿一个量法差去解释一个真实现象（replica 压腿处确实干涉，但**原因不是尺寸差**，它自己标「待补」）
- **⚠️ 订正本 wiki 4 处错值（其中 1 处安全相关）**：归档页 `_archive/entities/feetech-hd-1910.md` 记的是 **`1=GND · 2=Vcc · 3=Signal`** —— **那是 HL-2915 与 Dynamixel 的脚序**；同页的重量 **22.5 g 也是 HL-2915 的**（HD-1910 是 21 g）。另对比页把电压写成 5–8.4 V（应 4–8.4）、堵转写成 10 kg·cm（应 15@7.4V / 12@6V）。**这与 replica 记录的那个坑是同一个**（它也曾拿 `HL-2915` 那一行当「飞特接口惯例」去推荐 HD-1910）。间距防错让实物触发不了，但**自己压线就是烧舵机的一条路**
- **执行**：按 `_archive/README.md` 的「恢复到现行 = 移回并写回 index+log」——
  - **迁出并重写** `entities/feetech-hd-1910.md`（订正 4 处 + 三方对比 + 保护/反馈 + 开放项），删归档副本
  - **新建** `concepts/feetech-scs-bus.md`（协议 · 寄存器对照 · 符号位 · EEPROM 增益 · SDK · 实现接缝 · 对换执行器评估的意义）
  - **新建** `entities/microduck-replica.md`（承接两页的 wikilink，避免悬空）
  - **订正归档**：`comparisons/xl330-vs-feetech-servos.md`（表 + 订正note）· `entities/feetech.md` · `entities/feetech-hl-2909.md` 的 `5–8.4 V` · `_archive/INDEX.md`
- **对 RD05T 评估的反照（方法论收获）**：飞特把命题证成了实测——**即使协议全打通、15 颗能站起来，「走」仍要等重训**。所以 RD05T 的判定**不该卡在「协议不同怎么办」**，而应聚焦「**它到底是不是真 DXL、P 增益能否写**」，即 [[bam-identification-bench]] 的电气闸门与 `scripts/servo_swap_compare.py` 的守卫已在检的那两件事。一句话：**飞特是「已知的不同」，RD05T 是「未知的相同」**
- Updated: [[feetech-hd-1910]]（恢复为现行 · 重写）· [[feetech-scs-bus]]（新）· [[microduck-replica]]（新）· [[xl330-vs-feetech-servos]]（订正）· `_archive/entities/feetech.md` · `_archive/entities/feetech-hl-2909.md` · `_archive/INDEX.md` · [[index]] · `log.md`

## [2026-09-19] governance | 治理改造：3 份规则副本 → 单文件 ＋ 角色技能 ＋ 两台 linter
- **由来（Human）**：按 `tmp/solo-governance-playbook.md` 把本仓改造成**最简洁**的工程治理
- **盘点（改造前）**：治理 **504 行** —— `AGENTS.md` 18 ＋ `governance/agent-governance.md` 219 ＋ 通用模板 135 ＋ `.cursor/rules/*.mdc` 6 个共 132；同一套不变量写在 **3 处** = 漂移点。台账无 `wiki/tasks.md`，过程全在 GitHub（12 Issue · 1 Milestone · 0 PR）；**零机械校验**
- **定案四条（Human）**：角色 **4 个**（pm · hardware · software · structure，train 并入 software）· 删 `SCHEMA.md`（规范拆开）· GitHub **完全冻结** · 落 `governance/minimal` 分支待 review
- **规则收敛**：`AGENTS.md` 重写为 **93 行**（红线 6 条 · 改规则/技能/wiki 三行表 · 记录约定 ＋ 角色→必写记录表 · 角色表 · 仓库形态 · GitHub · 不收录）。红线新增「不代签 Gate」的具体项：上电 / 剪线改线 / 制板下单 / 烧录量产固件
- **角色换形态**：`.cursor/rules/*.mdc`（按 Issue 启停的短命职能）→ `.cursor/skills/<role>/SKILL.md`（**能自己进化**的操作手册 · `disable-model-invocation: true` 只许人唤起）。每个技能含「职能 · 记录 wiki · **不做** · 手册（具体命令与落点）· **沉淀区** · 红线」。**ros2 附件与 train 职能一并并入 software**（各保留一节，不再各占一个会话）
- **台账迁移**：新建 `wiki/tasks.md` —— #11（进行中）· 7 项（待办，含 #8）· 7 项（近 30 天已完成，带结论与落点）。历史 Issue #1–#11 与 Milestone `v0.1` **冻结保留只读**；[[diy-milestones]] 的过程面由 Issue 改指台账
- **`SCHEMA.md` 拆除**：frontmatter / 行数 / `raw/` 只读 → `AGENTS.md`「记录约定」（由 linter 机械执行）；领域 · 现行优先级 · 路径写法 · 标签表 · 页阈值 · 更新政策 → [[index]] 新增「wiki 规范」一节。**文件删除**（内容已搬，无第二副本）
- **旧治理归档不删**：`agent-governance.md` · 通用模板 · 6 个 rule → `_archive/governance/`（rule 改名 `rule-*.mdc` 以区分来源）＋ 该目录 README 写清**为什么停用**与新旧对照表。`upstreams.lock` ＋ `refresh-upstreams.ps1` 移到 `scripts/` —— 它们是**工具**不是规则（引用同步 3 处）
- **新增两台 linter（本步最省事、效果最大）**：`scripts/wiki_lint.py`（frontmatter · 行数 · 死链）＋ `scripts/refs_lint.py`（反引号与链接里的仓内路径）。判据都写在文件头
  - `refs_lint` 的关键机制：用 **`git check-ignore`** 自己判断「这个路径是不是本来就不该存在」—— `refs/` `temp/` `microduck_ros2/` 在干净克隆里**合法缺席**，不这么做 CI 天天报假错。路径判据**宁缺勿滥**：只认**首段命中仓库根真实条目**的片段（`scripts/dxl_ping.py` 查，上游仓内部的 `tof/src/sensor.rs` 不查）
  - 豁免一律按「**历史不该回溯失效**」立：`raw/` `_archive/` `assets/` 整体跳过 · `index`/`log`/`tasks` 免 frontmatter 与行数 · **`log.md` 另免死链** · `refs_lint` 不扫 `_archive/` 与 `log.md`
- **接 CI**：`.github/workflows/ci.yml` —— push / PR 到 `main` 跑两台 linter ＋ `compileall`
- **跑出来的真漂移（都是既有的，头一次被照出来，已全修）**：① `firmware-flash-matrix` 写「仓内 `scripts/flash_openocd.sh`」，实际在 `imu_to_dxl/scripts/` ② `imu-to-dxl-firmware-build` 的目录树把 `scripts/` 挂在仓根 ③ `entities/microduck-diy.md` 存的是 **UTF-8 BOM**（linter 改为读入即剥 BOM）④ `tmp/cam-*.jpg` 指向已移到 `temp/repo-tmp-2026-09-16/` 的旧路径 ⑤ 新技能手册里两处目录写错（`entities/imu-to-dxl-v2` · `concepts/seeed-bearings`）
- **超长页「不拆、改记账」（Human 定）**：[[hat-solder-kit]] **399** · [[xl330-vs-kpower-rd05t]] **220** · [[rd05t-vendor-inquiry-2026-09-18]] **203** 超 200 行上限。`wiki_lint.py` 加 `OVERSIZE_ACK` **只减不增**表（超记账值即 error；降到 ≤200 行则提示删条目），欠账记进 [[tasks]]。理由：第三页是**对外可发送件**（PDF 由本页生成），拆页就不成一封信了 —— 这类例外另行再定
- **同步引用 8 处**：根 `README.md`（新增「去哪找什么」＋「怎么干活」角色表）· [[index]]（承接 SCHEMA 的规范节）· [[local-workspace-layout]]（布局表重写，新增 `AGENTS.md` / `.cursor/skills/` / `.github/`）· [[diy-milestones]] · [[ros2-migration-plan]] · [[raw-inventory]] · `wiki/assets/README.md` · `scripts/README.md`（新增「目录一览」＋「两台 linter」两节）
- **`.gitignore`**：补回 `tmp/`（本地临时 —— 本轮那份蓝图就住在那里）
- **校验**：`wiki_lint` 61 页 **0 error / 3 warning**（3 条即上述记账）· `refs_lint` 76 文件 313 引用 **0 error**
- Updated: `AGENTS.md`（重写）· `.cursor/skills/{pm,hardware,software,structure}/SKILL.md`（新）· [[tasks]]（新）· [[index]] · [[local-workspace-layout]] · [[diy-milestones]] · [[ros2-migration-plan]] · [[raw-inventory]] · `README.md` · `scripts/README.md` · `scripts/wiki_lint.py`（新）· `scripts/refs_lint.py`（新）· `scripts/upstreams.lock` · `scripts/refresh-upstreams.ps1`（移入）· `.github/workflows/ci.yml`（新）· `.gitignore` · `_archive/governance/`（旧治理归档 ＋ README）· **删** `wiki/SCHEMA.md` · `log.md`

## [2026-09-19] pm | 现状收拢：焦点换挡到「整机装配 ＋ 供电链路」；台账 / 里程碑 / BOM 一次对齐
- **由来（Human）**：检查收拢当前情况 ＋ 下一步计划（6 项）
- **现状（本轮录入，均为口述事实）**：主控 · HAT · 机身 IMU · 系统镜像台架**均已完成**；机身 IMU 板 **焊 5 块 · 烧录 3 块**；**摄像头 2 颗**（Pi Cam V2 ＋ 亚博 IMX219）均已测；电池 **2 颗 ＋ 双充**；**降压模块到货**（5 V/15 A ×1 · 6 V/4 A ×2）；**舵机两批** —— 原厂单 [[robotis-xl330-order-2026-09-05]] **延误**（预计 **10 月中旬**可能发）· **闲鱼批** 5 国产组装 ＋ 9 原厂，预计 **09-21 周一**到；在途 VL53**L8CX** ToF ＋ 喇叭 **3525 4 Ω 3 W**（均 **09-23 周三**）；手柄用 Xbox（在手）＋ 可试亚博智能 PS2
- **焦点换挡**：原「HAT TTL [#11](https://github.com/ScrapMeta/microduck-diy/issues/11)（`0x55` 帧定论）」→ **整机装配 ＋ 供电链路 ＋ 官方软件联调**；#11 降为**承重项**（不阻塞主线）
- **台账**：[[tasks]] 重写 —— 进行中 6 项（叠装供电 · **直供对照** · #11 · 3 块 HAT · 官方软件联调 · IMU 竖装 `power_support`）＋ 待办 11 项（新增闲鱼到货装机 · 手柄冒烟 · 喇叭/ToF 到货先测 · 本轮物料事实落页）；已完成补 4 行（IMU 5/3 · 物料到货 ×3）
- **里程碑**：[[diy-milestones]] 新增「**物料到位（2026-09-19）**」表（8 行）＋ 母线 6.0 V 一句；v0.1 清单补勾 **#9**（回灌**不采用**），新增「整机装配 / 多板复现 / 官方软件联调 / 闲鱼装机」四项
- **BOM**：[[diy-bom]] §C 舵机行补两批状态与延误 · §E 状态列 ⏳→✅（主控 / HAT / 机身 IMU / 电池），新增「**降压模块**」一行
- **两处红线提醒（写进 [[tasks]]，pm 不代签 Gate）**：① **直供对照**属 **8.4 V > XL330 上限 6.0 V** 的**超规程**验证（[[dynamixel-xl330]]「母线电压天花板」），只作对照、**不作装机口径**；`Shutdown(63)` 清 bit0 后**再无过压保护** ② **上电 / 剪线改线 / 验收**只有 Human 能签
- **未做（改派，不越界）**：未建硬件实体页（降压模块型号 · 闲鱼订单 · 手柄页）→ 归 `/microduck-hardware`、`/microduck-software`；未替用户拍板 · 未扩范围
- **已确认（Human 2026-09-19）**：「闲鱼到货 ＋ 手中 **15 个**」= **闲鱼 14**（5 国产组装 ＋ 9 原厂）**＋ 现有 1** → 装机 **15 台**；原厂单到货后转备件
- **分支处置（Human 指示「只保留 main」）**：治理改造 commit → 本 wiki 收口 commit，**快进合并进 `main`**，`governance/minimal` 本地 ＋ 远端一并删除
- Updated: [[tasks]]（重写）· [[diy-milestones]] · [[diy-bom]] · [[index]]（现行焦点 ＋ 现行优先级）· `log.md`
