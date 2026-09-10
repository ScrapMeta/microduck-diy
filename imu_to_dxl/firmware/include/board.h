#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

void board_init(void);
void board_delay_ms(uint32_t ms);
uint32_t board_millis(void);

void board_dxl_set_tx(bool drive_bus);
void board_dxl_write(const uint8_t *data, size_t len);
bool board_dxl_read_byte(uint8_t *out);

int32_t board_imu_spi_write(void *user, uint8_t reg, const uint8_t *data, uint16_t len);
int32_t board_imu_spi_read(void *user, uint8_t reg, uint8_t *data, uint16_t len);

#ifdef __cplusplus
}
#endif
