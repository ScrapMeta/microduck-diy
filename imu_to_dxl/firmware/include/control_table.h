#pragma once
#include <stdint.h>
#include <stdbool.h>
#include "md_config.h"
#include "imu_pack.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t bytes[MD_CTRL_TABLE_SIZE];
} md_control_table_t;

void md_control_table_init(md_control_table_t *t);
void md_control_table_update_imu(md_control_table_t *t, const md_imu_sample_t *s);

#ifdef __cplusplus
}
#endif
