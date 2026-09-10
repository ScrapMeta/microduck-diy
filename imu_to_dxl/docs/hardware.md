# Hardware — imu_to_dxl_ref **v0.3**

> **现行 PCB / 原理图真源：**  
> `hardware/imu_to_dxl_ref_2026-08-30_18-59-47.eprj2`（嘉立创专业版）  
> 丝印：`imu-to-dxl v0.3` · 板框 **32×22 mm** · 四角 φ2.2 · 孔距 **29×19**  
> Wiki：`board-imu-to-dxl` · `imu-to-dxl-ref-schematic` · `imu-to-dxl-ref-bom` · `imu-to-dxl-ref-chip-wiring`  
> `_backup/` 与旧 `.epro2` **仅对照，勿覆盖定稿**。

总线契约（不变）：DXL **ID 200** · addr **124** · **1 Mbps** · PHY **SN74LVC1G125**。

---

## v0.3 vs v0.2（硬件）

| 项 | v0.2 | v0.3 |
|----|------|------|
| DXL 座 | 单 J1 EH | **J1 进 + J3 出**（并联） |
| 调试 | BM04 4P SWD；NRST→TP1 | **BM07 7P**（SWD+UART+NRST）；无 TP1 |
| 总线保护 | DATA 上 TVS | 座侧 **`DXL_BUS`**：D1 TVS + D2 5.1 V；**R6 150 Ω** → 芯片侧 **`DXL_DATA`** |
| 上拉 | 主要 R1 NRST | **R1–R5**：NRST / CS / OE# / DATA / UART_RX |
| 电源电容 | C1–C5 | +**C6 4.7 µF** on +3V3 |
| MCU 控制脚 | 同左（DXL/SPI/SWD） | **同**；另引出 **USART1** 到 J2 |

固件仍用 USART2+SPI1+PA1 OE#；USART1 仅调试口，可选启用。

---

## 连接器

### J1 / J3 · B3B-EH-A（DXL）

| Pin | 网名 |
|-----|------|
| 1 | GND |
| 2 | VBATT |
| 3 | DXL_BUS（DATA） |

叶节点可只插 **J1**，J3 空着。穿板 `VBATT` 宜 ≥40 mil / 铺铜。

### J2 · BM07B-SRSS-TB（调试 · LCSC **C160393**）

| Pin | 网名 | MCU | 丝印 |
|-----|------|-----|------|
| 1 | +3V3 | — | 3V3 |
| 2 | SWCLK | PA14 | CLK |
| 3 | SWDIO | PA13 | DIO |
| 4 | GND | — | GND |
| 5 | UART1_TX | **PA11** | TX |
| 6 | UART1_RX | **PA12**（R5↑） | RX |
| 7 | NRST | PF2-NRST（R1↑） | RST |

---

## MCU 脚位 ↔ 网络（firmware-relevant）

STM32G031F8P6 · TSSOP-20

| MCU 脚 | 信号名 | 网络 / 去向 |
|--------|--------|-------------|
| 4 | VDD | +3V3 |
| 5 | VSS | GND |
| 6 | PF2-NRST | NRST · J2-7 · R1↑ |
| 7 | PA0 | IMU_INT ← U1 INT1 |
| 8 | PA1 | **DXL_OE#** → U6 OE# · R3↑ |
| 9 | PA2 | **USART2_TX** → U6-A |
| 10 | PA3 | **USART2_RX** ← `DXL_DATA` · R4↑ |
| 11 | PA4 | SPI1_NSS / **SPI_CS** → U1 CS · R2↑ |
| 12 | PA5 | SPI1_SCK → U1 SCL |
| 13 | PA6 | SPI1_MISO ← U1 SDO |
| 14 | PA7 | SPI1_MOSI → U1 SDA |
| 16 | PA11 | **USART1_TX** → J2-5 |
| 17 | PA12 | **USART1_RX** ← J2-6 |
| 18 | PA13 | SWDIO → J2-3 |
| 19 | PA14 | SWCLK → J2-2 |
| 2 / 3 | PC14 / PC15 | LSE（Y1/C7/C8 **DNP**） |
| 1 / 15 / 20 | — | NC |

半双工规则：`PA1` 低 = U6 驱动总线（TX）；高 = 高阻（RX）。发完立即回 RX。

---

## 电源 / 保护

```
J1-2 ∥ J3-2 ── VBATT ──┬── U3 AP2210 VIN/EN
                       ├── C5 10µF 50V · C4 100n ── GND
U3 VOUT ── +3V3 ── C2 1µF · C6 4.7µF · MCU/IMU/U6/J2

J*.3 ── DXL_BUS ──┬── D1 PESD · D2 5V1 ── GND
                  └── R6 150Ω ── DXL_DATA ── U6-Y · PA3 · R4↑
```

---

## LSM6DSV16X SPI（DS13510）

| MCU | LSM6 脚 | 名 |
|-----|---------|-----|
| PA6 MISO | **1** | SDO/SA0 |
| PA7 MOSI | **14** | SDA |
| PA5 SCK | **13** | SCL |
| PA4 CS | **12** | CS（+ R2 10k↑） |
| GND | **2 / 3** | SDx / SCx（辅口，须接地） |

Gyro 满量程必须 **±500 dps**（与 `duck-control` 一致）。

---

## 时钟

TSSOP-20 无 HSE：默认 **HSI → PLL → 64 MHz**（或 bring-up 用 16 MHz HSI）。LSE 占位不焊。

---

## 仓路径

`microduck-diy/imu_to_dxl/`（已自 `microduck_imu_to_dxl/` 物理改名）。
