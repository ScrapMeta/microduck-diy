#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Host contract — must match duck-control / wiki board-imu-to-dxl */
#define MD_IMU_DXL_ID           200u
#define MD_IMU_BAUD             1000000u
#define MD_IMU_READ_ADDR        124u
#define MD_IMU_BLOCK_LEN        12u
#define MD_IMU_DIAG_LEN         8u
#define MD_IMU_MODEL_NUMBER     10200u
#define MD_IMU_FW_VERSION       1u

/* Control table size covering addr 0 .. 143 */
#define MD_CTRL_TABLE_SIZE      152u

/*
 * Board pin map — imu_to_dxl_ref **v0.3** (docs/hardware.md).
 * DXL/SPI/DIR pins unchanged from v0.2; J2 BM07 adds USART1 debug (optional).
 */
#define MD_PIN_IMU_INT          0u   /* PA0  ← LSM6 INT1 (optional poll) */
#define MD_PIN_DXL_OE           1u   /* PA1  → 1G125 OE# ; 0=TX 1=RX */
#define MD_PIN_USART2_TX        2u   /* PA2  AF1 */
#define MD_PIN_USART2_RX        3u   /* PA3  AF1 ← DXL_DATA */
#define MD_PIN_SPI_CS           4u   /* PA4 */
#define MD_PIN_SPI_SCK          5u   /* PA5  AF0 */
#define MD_PIN_SPI_MISO         6u   /* PA6  AF0 */
#define MD_PIN_SPI_MOSI         7u   /* PA7  AF0 */
#define MD_PIN_USART1_TX        11u  /* PA11 → J2-5 (debug, unused by default) */
#define MD_PIN_USART1_RX        12u  /* PA12 ← J2-6 */
#define MD_PIN_SWDIO            13u  /* PA13 → J2-3 */
#define MD_PIN_SWCLK            14u  /* PA14 → J2-2 */

/* Gyro full-scale for packing / LSM6 config — match duck-control ±500 dps */
#define MD_GYRO_FS_DPS          500

#ifdef __cplusplus
}
#endif
