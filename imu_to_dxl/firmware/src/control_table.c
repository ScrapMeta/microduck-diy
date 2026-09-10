#include "control_table.h"
#include <string.h>

void md_control_table_init(md_control_table_t *t)
{
    memset(t->bytes, 0, sizeof(t->bytes));
    /* Model Number */
    t->bytes[0] = (uint8_t)(MD_IMU_MODEL_NUMBER & 0xFF);
    t->bytes[1] = (uint8_t)((MD_IMU_MODEL_NUMBER >> 8) & 0xFF);
    t->bytes[2] = MD_IMU_FW_VERSION;
    t->bytes[7] = MD_IMU_DXL_ID;
    t->bytes[8] = 3;  /* baud 1 Mbps */
    t->bytes[9] = 0;  /* return delay */
    t->bytes[11] = 0; /* operating mode N/A */
}

void md_control_table_update_imu(md_control_table_t *t, const md_imu_sample_t *s)
{
    uint8_t block[MD_IMU_BLOCK_LEN];
    uint8_t diag[MD_IMU_DIAG_LEN];
    md_imu_pack12(s, block);
    md_imu_pack_diag(s, diag);
    memcpy(&t->bytes[MD_IMU_READ_ADDR], block, MD_IMU_BLOCK_LEN);
    memcpy(&t->bytes[MD_IMU_READ_ADDR + MD_IMU_BLOCK_LEN], diag, MD_IMU_DIAG_LEN);
}
