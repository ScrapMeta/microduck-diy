#include "imu_pack.h"
#include <string.h>

void md_imu_pack12(const md_imu_sample_t *s, uint8_t out[MD_IMU_BLOCK_LEN])
{
    out[0] = (uint8_t)(s->gyro_raw[0] & 0xFF);
    out[1] = (uint8_t)((s->gyro_raw[0] >> 8) & 0xFF);
    out[2] = (uint8_t)(s->gyro_raw[1] & 0xFF);
    out[3] = (uint8_t)((s->gyro_raw[1] >> 8) & 0xFF);
    out[4] = (uint8_t)(s->gyro_raw[2] & 0xFF);
    out[5] = (uint8_t)((s->gyro_raw[2] >> 8) & 0xFF);
    out[6] = (uint8_t)(s->quat_half[0] & 0xFF);
    out[7] = (uint8_t)((s->quat_half[0] >> 8) & 0xFF);
    out[8] = (uint8_t)(s->quat_half[1] & 0xFF);
    out[9] = (uint8_t)((s->quat_half[1] >> 8) & 0xFF);
    out[10] = (uint8_t)(s->quat_half[2] & 0xFF);
    out[11] = (uint8_t)((s->quat_half[2] >> 8) & 0xFF);
}

void md_imu_pack_diag(const md_imu_sample_t *s, uint8_t out[MD_IMU_DIAG_LEN])
{
    out[0] = (uint8_t)(s->sample_count & 0xFF);
    out[1] = (uint8_t)((s->sample_count >> 8) & 0xFF);
    out[2] = s->status;
    out[3] = 0;
    out[4] = (uint8_t)(s->accel_raw[0] & 0xFF);
    out[5] = (uint8_t)((s->accel_raw[0] >> 8) & 0xFF);
    out[6] = (uint8_t)(s->accel_raw[1] & 0xFF);
    out[7] = (uint8_t)((s->accel_raw[1] >> 8) & 0xFF);
}
