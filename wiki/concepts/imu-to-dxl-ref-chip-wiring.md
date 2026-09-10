---
title: imu_to_dxl 参考原理图 · 按芯片接线
created: 2026-09-03
updated: 2026-09-09
type: concept
tags: [imu, board, jlceda]
confidence: high
related: [imu-to-dxl-ref-schematic, imu-to-dxl-ref-bom, board-imu-to-dxl, dual-imu-board-selection, imu-to-dxl-v2]
---

# imu_to_dxl 参考原理图 · 按芯片接线

> **REFERENCE — NOT OFFICIAL**  
> 总览：[[imu-to-dxl-ref-schematic]]（**v0.3**）· BOM：[[imu-to-dxl-ref-bom]]。  
> **SPI：** 主口脚 **13/14**；辅口 **2/3→GND**（ST DS13510）。

## U1 · LSM6DSV16XTR

- **名称：** 六轴 IMU（加速度计 + 陀螺仪）  
- **说明：** 板端 **SFLP**；经 **SPI** 被 MCU 读取。LCSC C5267406。  
- **CS** 建议 **10 kΩ 上拉到 3V3**（上电锁定 SPI，防误入 I²C）。

```
              +3V3                    GND
                │    ┌── C1 100nF ──┐  │
                ├────┴──────────────┴──┤
     SPI_MISO ──┤1  SDO/SA0            │
          GND ──┤2  SDx（辅·须接地）   │
          GND ──┤3  SCx（辅·须接地）   │
      IMU_INT ──┤4  INT1               │
         +3V3 ──┤5  Vdd_IO             │
          GND ──┤6  GND                │
          GND ──┤7  GND         U1     │
         +3V3 ──┤8  Vdd      LSM6DSV   │
   INT2（可选）─┤9                     │
       SPI_CS ──┤12 CS ← 10k↑ +3V3     │
      SPI_SCK ──┤13 SCL（主 SPI 时钟） │
     SPI_MOSI ──┤14 SDA（主 SPI 数据） │
                └──────────────────────┘
```

| 脚 | 名 | 正确网络 | ~~旧错误~~ |
|----|----|----------|------------|
| 1 | SDO/SA0 | SPI_MISO | （同） |
| 2 | SDx | **GND** | ~~SPI_MOSI~~ |
| 3 | SCx | **GND** | ~~SPI_SCK~~ |
| 12 | CS | SPI_CS + 上拉 | （同，缺上拉） |
| 13 | SCL | **SPI_SCK** | ~~NC~~ |
| 14 | SDA | **SPI_MOSI** | ~~NC~~ |
| 4 | INT1 | IMU_INT → MCU-PA0 | |
| 5, 8 / 6, 7 | 电源 / 地 | +3V3 / GND | |

## U2 · STM32G031F8P6

- **名称：** DXL 从机 MCU  
- **说明：** 跑 Protocol 2.0（ID **200**）、读 U1、经 U6 半双工上总线。TSSOP-20 **无 HSE**；主钟 **HSI→PLL**。复位脚丝印为 **PF2-NRST**。LCSC C529334。

```
                ┌──────────────────────────────┐
  X1-OSC1 ──────┤2  PC14-OSC32_IN              │
  X1-OSC2 ──────┤3  PC15-OSC32_OUT             │
         +3V3 ──┤4  VDD     U2 STM32G031       │
          GND ──┤5  VSS                        │
   R1←── NRST ──┤6  PF2-NRST → J2-7            │
      IMU_INT ──┤7  PA0                        │
          PA1 ──┤8  PA1 → U6 OE# · R3↑         │
    USART2_TX ──┤9  PA2 → U6 A                 │
     DXL_DATA ──┤10 PA3 ← 总线 RX · R4↑        │
   SPI PA4–7 ───┤11–14 CS/SCK/MISO/MOSI (+R2↑CS)│
   USART1_TX ───┤16 PA11 → J2-5                │
   USART1_RX ───┤17 PA12 ← J2-6 · R5↑          │
        SWDIO ──┤18 PA13 → J2-3                │
        SWCLK ──┤19 PA14 → J2-2                │
           NC ──┤1,15,20                       │
                └──────────────────────────────┘
         +3V3 ── C3 100nF ── GND（近 pin4/5）
```

| 脚 | 名 | 网络 |
|----|----|------|
| 6 | PF2-NRST | NRST ← R1 ← +3V3 · J2-7 |
| 8–10 | PA1/2/3 | OE# / TX / DXL_DATA |
| 11–14 | PA4–7 | SPI |
| 16–17 | PA11/12 | USART1 → J2 TX/RX |
| 18–19 | PA13/14 | SWDIO / SWCLK |
| 2–3 | PC14/15 | LSE（Y1，DNP） |

## U3 · AP2210K-3.3TRG1

- **名称：** 3.3 V LDO  
- **说明：** `VBATT`（DXL 母线约 6.6–8.2 V）降压供逻辑；**EN 与 IN 同接 VBATT** 常开。Vin≤**13.2 V**。LCSC **C176959**。pin4 BYP 可悬空。OUT 旁路 **≥1 µF（C2=C52923）**。  
  ~~勿用 TLV75533（Vin 仅 5.5 V）。~~

```
     VBATT ──┬── C4 100nF / C5 10µF ── GND
             ├── U3-1 VIN、U3-3 EN
             │    ┌─────────────────┐
             └────┤1 VIN            │
          GND ────┤2 GND    U3      │
     VBATT ───────┤3 EN   AP2210K   │
           NC ────┤4 BYP            │
         +3V3 ←───┤5 VOUT ── C2 1µF ── GND
                  └─────────────────┘
```

| 脚 | 名 | 网络 |
|----|----|------|
| 1 / 3 | VIN / EN | VBATT |
| 2 / 5 | GND / VOUT | GND / +3V3 |
| 4 | BYP | NC（可悬空） |

## U6 · 74LVC1G125

- **名称：** DXL 半双工三态缓冲（参考 PHY）  
- **说明：** DATA 单线；TX 时把 PA2 推上总线，RX 时输出高阻，PA3 听总线。OE# 由 PA1 控制。**非官方还原。** 封装 **SOT-23-5（DBV）**，LCSC **C3040625**（与 HAT U6 同料；勿换成 126）。

```
         +3V3 ──┤5 VCC
          PA1 ──┤1 OE#     U6 74LVC1G125
    USART2_TX ──┤2 A
          GND ──┤3 GND
     DXL_DATA ←─┤4 Y ── J1-3、D1、U2-PA3
```

| 脚 | 名 | 网络 |
|----|----|------|
| 1 / 2 / 4 | OE# / A / Y | PA1 / USART2_TX / DXL_DATA |
| 3 / 5 | GND / VCC | GND / +3V3 |

## Y1 · Q13FC13500004（32.768 kHz）+ C7 / C8

- **名称：** LSE 晶振（可选）  
- **说明：** 仅接 U2 **OSC32**（RTC）。**默认 DNP**；主钟 / 1 Mbps 用 **HSI**，不焊即可。焊接后固件仅在需要 RTC 时开 LSE，UART 仍走 HSI。LCSC C32346；C7/C8 = 12 pF C1547。

```
   X1-OSC1 ── Y1 一端 ── C7 12pF ── GND ── U2-2 PC14
   X1-OSC2 ── Y1 另一端 ── C8 12pF ── GND ── U2-3 PC15
```

## J1 · B3B-EH-A + D1 · PESD5V0S1BA

- **名称：** Dynamixel TTL 3P 座（JST EH）+ DATA 线 TVS  
- **说明：** 官方 XL330 配套为 **JST EHR-03 / PCB 座 B3B-EH-A**（2.5 mm），可插 Robot Cable-X3P。**勿用 JST-PH 2.0 mm。** 直插通孔。D1 近座。LCSC **C160259**（与 HAT 同料）；D1 C2827694。

```
  J1-1 GND ──────── GND（∥ J3-1）
  J1-2 VBATT ────── U3-IN/EN、C4、C5（∥ J3-2）
  J1-3 DATA ── DXL_BUS ──┬── D1 / D2 ── GND
                         └── R6 ── DXL_DATA → U6-Y、U2-PA3、R4↑
```

## J2 · BM07B-SRSS-TB（调试 7P）

- **名称：** SWD + UART + NRST（JST SH 1.0 · **7P**）  
- **说明：** LCSC **C160393**（BM07B-SRSS-TB）。替 v0.2 的 BM04 4P + TP1。R1=NRST↑ · R5=UART1_RX↑。

```
  1 +3V3 · 2 SWCLK · 3 SWDIO · 4 GND · 5 UART1_TX · 6 UART1_RX · 7 NRST
  丝印：J2 ●3V3 CLK DIO GND TX RX RST
```

相关：[[imu-to-dxl-ref-schematic]] · [[imu-to-dxl-ref-bom]] · [[board-imu-to-dxl]] · [[imu-to-dxl-v2]]
