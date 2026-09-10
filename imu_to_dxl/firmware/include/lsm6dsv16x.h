#pragma once
#include <stdint.h>
#include <stdbool.h>
#include "imu_pack.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef int32_t (*md_spi_write_reg_fn)(void *user, uint8_t reg, const uint8_t *data, uint16_t len);
typedef int32_t (*md_spi_read_reg_fn)(void *user, uint8_t reg, uint8_t *data, uint16_t len);
typedef void (*md_delay_ms_fn)(uint32_t ms);

typedef struct {
    void *user;
    md_spi_write_reg_fn write;
    md_spi_read_reg_fn read;
    md_delay_ms_fn delay_ms;
    bool present;
    bool sflp_live;
    uint16_t sample_count;
    md_imu_sample_t last;
} md_lsm6_t;

/** Probe WHO_AM_I, configure ±500 dps / SFLP game rotation @ ~60 Hz into FIFO. */
bool md_lsm6_init(md_lsm6_t *dev);

/** Drain FIFO / read gyro; update `dev->last`. Returns true if sample refreshed. */
bool md_lsm6_poll(md_lsm6_t *dev);

#ifdef __cplusplus
}
#endif
