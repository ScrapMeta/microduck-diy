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

