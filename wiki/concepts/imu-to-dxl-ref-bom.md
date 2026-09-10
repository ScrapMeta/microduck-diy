---
title: imu_to_dxl 参考板 BOM（机身 · v0.3）
created: 2026-09-03
updated: 2026-09-09
type: concept
tags: [imu, board, bom, jlceda]
sources:
  - concepts/imu-to-dxl-ref-schematic.md
  - concepts/board-imu-to-dxl.md
  - concepts/imu-to-dxl-lcsc-order-2026-09-09.md
  - concepts/imu-to-dxl-lcsc-order-2026-09-05.md
confidence: high
related:
  - imu-to-dxl-ref-schematic
  - imu-to-dxl-ref-chip-wiring
  - imu-to-dxl-ref-pcb-layout
  - board-imu-to-dxl
  - dual-imu-board-selection
  - imu-to-dxl-v2
  - diy-bom
  - imu-to-dxl-lcsc-order-2026-09-09
  - imu-to-dxl-lcsc-order-2026-09-05
  - imu-to-dxl-replica-bom
  - elec-three-board-bom
---

# imu_to_dxl 参考板 BOM（机身 · **v0.3**）

> **REFERENCE — NOT OFFICIAL。** 嘉立创工程定稿 **v0.3**（2026-09-09）：**1 号大板 32×22** · 双 EH · BM07 调试。  
> 协议：DXL ID **200** · addr **124** · PHY **1G125** · [[imu-to-dxl-v2]]。  
> 板卡总览：[[board-imu-to-dxl]]。v0.2 及更早见文末。

| 项 | 值 |
|----|-----|
| 丝印 | **`imu-to-dxl v0.3`** |
| 板框 | **32 × 22 mm** · 四角 φ2.2 · 孔距 **29 × 19** |
| 必贴 | **24** |
| DNP | **3**（Y1、C7、C8） |
| 相对 v0.2 | +J3 · J2→BM07 · +D2/R6/C6 · +R2–R5 · −TP1 |

## 有源 / 连接器

| Ref | 型号 | LCSC | Qty | 封装 | 贴装 | 说明 |
|-----|------|------|-----|------|------|------|
| U1 | LSM6DSV16XTR | C5267406 | 1 | LGA-14 | 必贴 | SPI + SFLP |
| U2 | STM32G031F8P6 | C529334 | 1 | TSSOP-20 | 必贴 | 主钟 HSI→PLL |
| U3 | AP2210K-3.3TRG1 | C176959 | 1 | SOT-23-5 | 必贴 | Vin≤13.2 V；EN=IN=VBATT |
| U6 | SN74LVC1G125DBVR-TP | C3040625 | 1 | SOT-23-5 | 必贴 | 与 HAT U6 同料 |
| D1 | PESD5V0S1BA | C2827694 | 1 | SOD-323 | 必贴 | `DXL_BUS` TVS · 近座 |
| D2 | BZT52C5V1S-7-F | **C151348** | 1 | SOD-323 | 必贴 | `DXL_BUS` 5.1 V 钳位（与 HAT 同料） |
| J1 | B3B-EH-A | C160259 | 1 | TH EH 2.5 | 必贴 | 进 · 1=GND 2=VBATT 3=DATA |
| J3 | B3B-EH-A | C160259 | 1 | TH EH 2.5 | 必贴 | 出 · 与 J1 并联 |
| J2 | BM07B-SRSS-TB | **C160393** | 1 | SH 1.0 **7P** | 必贴 | 立创匹配料号；旧写 C20089159 同系列 |
| Y1 | Q13FC13500004 32.768 kHz | C32346 | 1 | 3215 | **DNP** | LSE 占位 |

### J2 针脚 / 丝印

| Pin | 网名 | 丝印缩写 |
|-----|------|----------|
| 1 | +3V3 | 3V3 |
| 2 | SWCLK | CLK |
| 3 | SWDIO | DIO |
| 4 | GND | GND |
| 5 | UART1_TX | TX |
| 6 | UART1_RX | RX |
| 7 | NRST | RST |

丝印示例：`J2` · `●3V3 CLK DIO GND TX RX RST`

## 无源

| Ref | 值 | LCSC | Qty | 封装 | 贴装 | 说明 |
|-----|-----|------|-----|------|------|------|
| C1 | 100 nF | C1525 | 1 | 0402 | 必贴 | +3V3 · 近 U1 |
| C2 | 1 µF | C52923 | 1 | 0402 | 必贴 | U3-OUT |
| C3 | 100 nF | C1525 | 1 | 0402 | 必贴 | +3V3 · 近 U2 |
| C4 | 100 nF | **C307331** | 1 | 0402 | 必贴 | VBATT · 近 U3-IN（与 C1525 可互换） |
| C5 | 10 µF 50 V | C440198 | 1 | 0805 | 必贴 | VBATT bulk · 贴 U3 |
| C6 | 4.7 µF | **C19666** | 1 | 0603 | 必贴 | +3V3 bulk |
| C7 | 12 pF C0G | C1547 | 1 | 0402 | **DNP** | Y1 |
| C8 | 12 pF C0G | C1547 | 1 | 0402 | **DNP** | Y1 |
| R1 | 10 kΩ | C25744 | 1 | 0402 | 必贴 | NRST↑ |
| R2 | 10 kΩ | C25744 | 1 | 0402 | 必贴 | SPI_CS↑ · 近 U1 |
| R3 | 10 kΩ | C25744 | 1 | 0402 | 必贴 | DXL_OE#↑ |
| R4 | 10 kΩ | C25744 | 1 | 0402 | 必贴 | DXL_DATA↑ · 芯片侧 |
| R5 | 10 kΩ | C25744 | 1 | 0402 | 必贴 | UART1_RX↑ |
| R6 | 150 Ω | **C22808** | 1 | 0603 | 必贴 | DXL_BUS↔DXL_DATA |

## 采购合并（单板）

| LCSC | 型号/值 | 单板 | 备注 |
|------|---------|------|------|
| C5267406 | LSM6DSV16XTR | 1 | 淘宝已有库存可复用 |
| C529334 | STM32G031F8P6 | 1 | 同上 |
| C176959 | AP2210K-3.3 | 1 | `SO26090520116` 已订 |
| C3040625 | SN74LVC1G125 | 1 | 已订 |
| C2827694 | PESD5V0S1BA | 1 | 已订 |
| **C151348** | BZT52C5V1S | 1 | **新增**；HAT 同料可合并 |
| C160259 | B3B-EH-A | **2** | 已订×10；本板用 2 |
| **C160393** | BM07B-SRSS-TB | 1 | J2；配单匹配；**订单未订** |
| C1525 | 100 nF 0402 | **2** | C1/C3 |
| C307331 | 100 nF 0402 | **1** | C4（配单） |
| C52923 | 1 µF 0402 | 1 | C2 · LDO OUT |
| **C440198** | 10 µF 50V 0805 | 1 | VBATT；勿用 C1691 |
| **C19666** | 4.7 µF 0603 | 1 | +3V3 bulk |
| C25744 | 10 kΩ 0402 | **5** | R1–R5 |
| **C22808** | 150 Ω 0603 | 1 | R6 |

## 采购实绩

| 单 | 说明 |
|----|------|
| **BOM `BOM260909006316`** | **v0.3 正确配单** · 5 套报价 ¥195.02 → [[imu-to-dxl-lcsc-order-2026-09-09]] |
| **`SO26090921960`**（2026-09-09） | **v0.3 实购** · ¥112.58 · 含 MCU×2+IMU×2+…；**无 BM07** |
| `SO26090520116`（2026-09-05） | 早期 ref → [[imu-to-dxl-lcsc-order-2026-09-05]] |

**仍缺：BM07B J2（下单用 C160393）**。  
误传配单 `BOM260909006112`（replica）作废，不以之为 v0.3 源。

相对早期 `SO26090520116`：v0.3 已覆盖 D2/R6/C6/核心 IC；**不必再买** BM04、TP1。

## 相对 v0.2 变更摘要

| 变更 | 说明 |
|------|------|
| 板框 | ~25×17 → **32×22**（1 号测试定稿） |
| J3 | 第二只 EH，菊花链 |
| J2 | BM04 4P → **BM07 7P**（+UART +NRST） |
| 保护 | +D2 钳位 · +R6 串阻；网分 `DXL_BUS` / `DXL_DATA` |
| 上拉 | +R2 CS · +R3 OE# · +R4 DATA · +R5 UART_RX |
| 电源 | +C6 4.7 µF on +3V3 |
| 删除 | TP1（NRST 进 J2.7） |

## 首板贴装

1. 必贴全部有源 + C1–C6 + R1–R6 + J1/J2/J3。  
2. Y1/C7/C8 **不焊**。  
3. 叶节点可只插 **J1**，J3 空着。

旧采购记录：[[imu-to-dxl-lcsc-order-2026-09-05]]。

相关：[[board-imu-to-dxl]] · [[imu-to-dxl-ref-schematic]] · [[diy-bom]] · [[imu-to-dxl-v2]]
