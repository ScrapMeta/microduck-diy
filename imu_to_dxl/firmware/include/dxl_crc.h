#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint16_t md_dxl_crc16(const uint8_t *data, uint16_t len);

#ifdef __cplusplus
}
#endif
