---
title: imu_to_dxl 参考原理图
created: 2026-09-01
updated: 2026-09-09
type: concept
tags: [imu, board, jlceda]
confidence: high
related:
  - dual-imu-board-selection
  - imu-to-dxl-v2
  - board-imu-to-dxl
  - imu-to-dxl-ref-chip-wiring
  - imu-to-dxl-ref-bom
  - imu-to-dxl-ref-pcb-layout
---

# imu_to_dxl 参考原理图

> **REFERENCE — NOT OFFICIAL**  
> **现行：`imu-to-dxl v0.3`（2026-09-09）。** ID **200** · addr **124** · LSM6 + SFLP · PHY **1G125**。  
> **硬件文档真源（仓内）：** `imu_to_dxl/docs/hardware.md` · 工程 `imu_to_dxl/hardware/imu_to_dxl_ref_2026-08-30_18-59-47.eprj2`  

## v0.3 审图结论

| 块 | 结论 |
|----|------|
| 电源 | J1∥J3 `VBATT` → U3 → `+3V3`；C4/C5@IN · C2@OUT · C6@3V3 |
| DXL | 座侧 `DXL_BUS`（D1/D2/J1.3/J3.3/R6）↔ 芯片侧 `DXL_DATA`（U6-Y/PA3/R4↑） |
| PHY | PA1=`DXL_OE#`+R3↑ · PA2→U6-A · U6=1G125 |
| SPI | 辅口 2/3→GND；主 SPI 13/14；CS+R2↑ |
| 调试 | J2 BM07 7P（含 NRST）；无 TP1 |
| DNP | Y1/C7/C8 |

## 器件摘要

| Ref | 型号 | 作用 |
|-----|------|------|
| U1 / U2 / U3 / U6 | LSM6 · G031 · AP2210 · 1G125 | 核心 |
| D1 / D2 | PESD · BZT52C5V1S | `DXL_BUS` 保护 |
| J1 / J3 | B3B-EH-A ×2 | 进 / 出 |
| J2 | BM07B 7P | 3V3 CLK DIO GND TX RX RST |
| R1–R5 / R6 | 10k×5 / 150Ω | 上拉 / 串阻 |
| C1–C6 · Y1/C7/C8 | 见 BOM | 去耦；LSE DNP |

## 网络名

| 网络 | 连接 |
|------|------|
| `VBATT` | J1-2 · J3-2 · U3-IN/EN · C4 · C5 |
| `+3V3` | U3-OUT · U1/U2/U6 · C1–C3 · C6 · J2-1 · R1–R5 |
| `DXL_BUS` | J1-3 · J3-3 · D1 · D2 · R6 |
| `DXL_DATA` | R6 · U6-Y · U2-PA3 · R4↑ |
| `DXL_OE#` | U2-PA1 · U6-OE# · R3↑ |
| `USART2_TX` | U2-PA2 → U6-A |
| `SPI_*` | U2 ↔ U1（+ R2 on CS） |
| `IMU_INT` | U1-INT1 → U2-PA0 |
| `SWDIO`/`SWCLK`/`UART1_*`/`NRST` | J2 ↔ U2（R1 on NRST · R5 on RX） |
| `X1-OSC*` | Y1 ↔ PC14/15（DNP） |

## 电源

```
J1-2 / J3-2 ── VBATT ──┬── U3 VIN/EN
                       ├── C5 10µF / C4 100n ── GND
U3 VOUT ── +3V3 ── C2 1µF · C6 4.7µF · 逻辑供电
```

## DXL

```
J*.3 ── DXL_BUS ──┬── D1 TVS / D2 5V1 ── GND
                  └── R6 150Ω ── DXL_DATA ──┬── U6-Y
                                           ├── U2-PA3
                                           └── R4↑ +3V3
PA2 → U6-A · PA1 → OE# (+ R3↑)
```

## SPI（正确脚）

| U1 | 脚 | U2 | 网络 |
|----|----|-----|------|
| CS | 12 | PA4 | SPI_CS + R2↑ |
| SCL | 13 | PA5 | SPI_SCK |
| SDA | 14 | PA7 | SPI_MOSI |
| SDO | 1 | PA6 | SPI_MISO |
| SDx/SCx | 2/3 | — | **GND** |

## 软件契约

```
imu-to-dxl v0.3 · REFERENCE · NOT OFFICIAL
DXL 2.0 · ID 200 · 1 Mbps · sync_read @124 · 12B
gyro ±500 dps + quat half · SFLP · mount ≈ [+z,+y,-x]
```

相关：[[imu-to-dxl-ref-bom]] · [[imu-to-dxl-ref-chip-wiring]] · [[board-imu-to-dxl]] · [[imu-to-dxl-v2]]
