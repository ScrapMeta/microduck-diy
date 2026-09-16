---
title: 三板电子 BOM 定稿（HAT + 机身 + 头）
created: 2026-09-05
updated: 2026-09-06
type: concept
tags: [bom, hat, imu, procurement, final]
sources:
  - concepts/imu-to-dxl-ref-bom.md
  - concepts/head-imu-ref-bom.md
  - ../refs/elec_RPI_Robot_HAT/production/ASE01187-C1_elec_RPI_Robot_HAT_BOM.csv
confidence: high
related:
  - elec-three-boards
  - board-hat
  - board-imu-to-dxl
  - imu-to-dxl-ref-bom
  - elec-rpi-robot-hat
  - diy-bom
---

# 三板电子 BOM 定稿

> **状态：定稿。** HAT 器件锁定；机身按 v0.3 网表。头 IMU = HAT BMI088（无独立头专板）。  
> 整机数量默认各 **×1**。DNP 默认不买。CSV：[`assets/bom/three-board-final-bom.csv`](../assets/bom/three-board-final-bom.csv)  
> **CAD / 规格速查：** [[elec-three-boards]]（[[board-hat]] · [[board-imu-to-dxl]]）

| 板 | 工程 / 源 | 角色 | 信息卡 |
|----|-----------|------|--------|
| **HAT** | `ASE01187-C1_elec_RPI_Robot_HAT_BOM.csv` | 主控扩展 · **锁定** · 含头 BMI088 | [[board-hat]] |
| **机身** | [[imu-to-dxl-ref-bom]] | DXL 从机 IMU · ID 200 | [[board-imu-to-dxl]] |

---

## A. 机身 imu_to_dxl（必贴）

| Ref | 型号 | LCSC | Qty | 封装 | 说明 |
|-----|------|------|-----|------|------|
| U1 | LSM6DSV16XTR | C5267406 | 1 | LGA-14 | SPI + SFLP |
| U2 | STM32G031F8P6 | C529334 | 1 | TSSOP-20 | DXL 从机 |
| U3 | AP2210K-3.3TRG1 | C176959 | 1 | SOT-23-5 | VBATT→3V3（Vin≤13.2 V） |
| U6 | SN74LVC1G125DBVR-TP | C3040625 | 1 | SOT-23-5 | 半双工 OE#；与 HAT U6 同 |
| D1 | PESD5V0S1BA | C2827694 | 1 | SOD-323 | DATA TVS |
| J1 | B3B-EH-A | C160259 | 1 | EH 2.5 3P | 与 HAT 同；GND/VBATT/DATA |
| J2 | BM04B-SRSS-TB | C160390 | 1 | SH 1.0 4P | SWD；与 HAT/头同；无 NRST |
| C1,C3,C4 | 100 nF | C1525 | 3 | 0402 | 去耦 |
| C2 | 1 µF | C52923 | 1 | 0402 | LDO OUT |
| C5 | 10 µF 50 V | C440198 | 1 | 0805 | VBATT bulk（勿用 C1691） |
| R1 | 10 kΩ | C25744 | 1 | 0402 | NRST 上拉 → TP1 |

**DNP（可不买）：** Y1 C32346；C7/C8 12 pF C1547×2。

---

## C. HAT（完整 · 锁定）

源表：`refs/elec_RPI_Robot_HAT/production/ASE01187-C1_elec_RPI_Robot_HAT_BOM.csv`（含 DNP 行）。

| LCSC | 型号 / 值 | Qty | 备注 |
|------|-----------|-----|------|
| C52923 | 1 µF 0402 | 15 | |
| C307331 | 100 nF 0402 | 13 | 多数去耦 |
| C1525 | 100 nF 0402 | 3 | 与 IMU 可合并买 |
| C1691 | 10 µF 0603 | 5 | 仅 3V3 侧 |
| C72488 | 10 µF 63 V 电解 | 1 | |
| C84419 | 22 µF 6.3 V 0603 | 2 | |
| C15195 | 10 nF 0402 | 2 | |
| C71693 | 220 nF 0402 | 2 | |
| C78606 | BAT54W | 1 | |
| C19077392 | 3V3 Zener | 1 | |
| C151348 | 5V1 | 1 | |
| C76884 | FB 600Ω | 1 | |
| C88970 | FB 120Ω | 2 | |
| C2765060 | Wago-2 | 3 | |
| C160258 | B4B-EH-A | 2 | DXL 4P |
| C160259 | B3B-EH-A | 2 | DXL 3P |
| C2685112 | 2×20 HAT 座 | 1 | |
| C160390 | BM04B-SRSS-TB | 4 | STEMMA |
| C57254 | 6.8 µH | 1 | |
| C7587901 | MEMS 麦 | 1 | |
| C727128 | MMBT3906 | 1 | |
| C142518 | SI2312 | 1 | |
| C25744 | 10 kΩ 0402 | 19 | |
| C17168 | 0 Ω 0402 | 11 | |
| C25765 | 20 kΩ | 1 | |
| C138054 | 150 Ω | 1 | |
| C2906860 | 100 Ω | 1 | |
| C913703 | 100 Ω NTC | 1 | |
| C86270 | PAM8406D | 1 | |
| C473393 | LM5050-1 | 1 | |
| C194919 | BMI088 | 1 | HAT IMU（控制环不用） |
| C181753 | TLV320AIC3104 | 1 | |
| C347373 | XC6206P182MR | 1 | |
| C7666 | 74LVC1G08 | 1 | |
| C3040625 | SN74LVC1G125 | 1 | 与机身同 |
| C7834 | SN74LVC1G126 | 1 | 仅 HAT |
| C2922535 | SIT3088E | 1 | |
| C2071056 | AP63205 | 1 | |
| C7425459 | 12 MHz 晶振 | 1 | |

HAT DNP（表内已标）：C25、R10/R11、R16/R17/R41、R36/R37、U4 等按 CSV。

---

## D. 整机采购合并（×1 套 · 仅必贴）

按 LCSC 加总；机身晶体默认不计入。头 IMU = HAT BMI088，无独立头专板用量。

| LCSC | 型号 | 机身 | HAT | **合计** |
|------|------|------|-----|----------|
| C5267406 | LSM6DSV16XTR | 1 | — | **1** |
| C160390 | BM04B-SRSS-TB | 1 | 4 | **5** |
| C160259 | B3B-EH-A | 1 | 2 | **3** |
| C1525 | 100 nF 0402 | 3 | 3 | **6** |
| C52923 | 1 µF 0402 | 1 | 15 | **16** |
| C25744 | 10 kΩ 0402 | 1 | 19 | **20** |
| C3040625 | SN74LVC1G125 | 1 | 1 | **2** |
| C529334 | STM32G031F8P6 | 1 | — | **1** |
| C176959 | AP2210K-3.3 | 1 | — | **1** |
| C2827694 | PESD5V0S1BA | 1 | — | **1** |
| C440198 | 10 µF 50V 0805 | 1 | — | **1** |
| C7834 | SN74LVC1G126 | — | 1 | **1** |
| C307331 | 100 nF 0402 | — | 13 | **13** |
| … | HAT 其余见 §C | — | 按 CSV | |

**不要合并：** C440198↔C1691（耐压）；C3040625↔C7834（OE 极性）；机身 LSM6↔HAT BMI088。

---

## E. 定稿决策摘要

| 决策 | 结果 |
|------|------|
| 机身 LDO | **AP2210K-3.3** |
| 机身 LDO OUT | **1 µF C52923** |
| STEMMA / 调试座 | **BM04B C160390**（机身 SWD 已升 BM07，见 v0.3） |
| 机身 10 µF | **C440198 50 V** |
| 半双工 | 机身/HAT 共用 **1G125**；HAT 另有 **1G126** |
| 头 IMU | HAT **BMI088** |

分板明细：[[imu-to-dxl-ref-bom]] · HAT CSV。  
相关：[[elec-three-boards]] · [[diy-bom]] · [[imu-to-dxl-ref-schematic]]
