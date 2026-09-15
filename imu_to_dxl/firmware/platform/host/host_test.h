#pragma once
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

void host_dxl_feed(const uint8_t *data, size_t len);
size_t host_dxl_last_tx(uint8_t *out, size_t max);
void host_dxl_clear_tx(void);
bool host_dxl_is_driving(void);
unsigned host_dxl_tx_transitions(void);

#ifdef __cplusplus
}
#endif
