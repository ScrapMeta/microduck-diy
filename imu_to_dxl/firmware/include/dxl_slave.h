#pragma once
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "md_config.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*md_dxl_set_tx_fn)(bool drive_bus);
typedef void (*md_dxl_write_bytes_fn)(const uint8_t *data, size_t len);

typedef struct {
    uint8_t id;
    uint8_t *table;
    uint16_t table_size;
    md_dxl_set_tx_fn set_tx;
    md_dxl_write_bytes_fn write_bytes;
    /* RX parser */
    uint8_t rx[64];
    uint16_t rx_len;
    uint8_t state;
    uint16_t expect_len;
} md_dxl_slave_t;

void md_dxl_slave_init(md_dxl_slave_t *s,
                       uint8_t id,
                       uint8_t *table,
                       uint16_t table_size,
                       md_dxl_set_tx_fn set_tx,
                       md_dxl_write_bytes_fn write_bytes);

/** Feed one UART RX byte. May transmit a status packet. */
void md_dxl_slave_on_byte(md_dxl_slave_t *s, uint8_t b);

#ifdef __cplusplus
}
#endif
