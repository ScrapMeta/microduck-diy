# Protocol — imu_to_dxl ↔ HAT / duck-control

## Bus

- TTL half-duplex on HAT Dynamixel port（与舵机共线）
- Protocol **2.0** · **1 Mbps** · ID **200**
- 每 tick：`sync_read` 地址 **124**、长度 **12**；IMU ID **排在舵机之前**

## Block @ 124（12 B）

| Offset | Type | Meaning |
|--------|------|---------|
| 0..1 | `i16` LE | gyro X，±500 dps，17.5 mdps/LSB |
| 2..3 | `i16` LE | gyro Y |
| 4..5 | `i16` LE | gyro Z |
| 6..7 | `u16` LE | quat X，IEEE binary16 |
| 8..9 | `u16` LE | quat Y |
| 10..11 | `u16` LE | quat Z |

主机：`w = sqrt(max(0, 1 − x² − y² − z²))`。全零 half 字 = SFLP 未就绪（保持上一姿态）。

## Optional diagnostic @ 136（本固件扩展，主机控制环不读）

| Offset | Type | Meaning |
|--------|------|---------|
| 0..1 | `u16` | sample counter |
| 2 | `u8` | status flags（bit0 IMU ok · bit1 SFLP live） |
| 3 | `u8` | reserved |
| 4..7 | `i16`×2 | accel X/Y（±4 g raw，可选） |

完整 20 B 官方布局未公开；扩展字段勿假定与量产板一致。

## Instructions handled

| Inst | Code | Behavior |
|------|------|----------|
| Ping | 0x01 | Status, 0 params |
| Read | 0x02 | Status + control table slice |
| Sync Read | 0x82 | If ID in list → Status + slice（本板通常第一） |
| Write | 0x03 | 仅允许少数 EEPROM 区（如 return delay）；忽略危险写 |

## DIR / OE#

`PA1` → 74LVC1G125 `OE#`：**0 = 驱动总线（TX）**，**1 = 高阻（RX）**。发完立即回到 RX。
