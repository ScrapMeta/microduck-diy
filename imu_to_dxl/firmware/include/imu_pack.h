#pragma once
#include <stdint.h>
#include "md_config.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int16_t gyro_raw[3];     /* ±500 dps counts */
    uint16_t quat_half[3];   /* x,y,z binary16; 0,0,0 = not ready */
    uint16_t sample_count;
    uint8_t status;          /* bit0 whoami ok · bit1 sflp live */
    int16_t accel_raw[3];    /* optional diag */
} md_imu_sample_t;

/** Pack control-loop 12-byte block @ addr 124. */
void md_imu_pack12(const md_imu_sample_t *s, uint8_t out[MD_IMU_BLOCK_LEN]);

/** Pack optional 8-byte diagnostic immediately after the 12-byte block. */
void md_imu_pack_diag(const md_imu_sample_t *s, uint8_t out[MD_IMU_DIAG_LEN]);

#ifdef __cplusplus
}
#endif
