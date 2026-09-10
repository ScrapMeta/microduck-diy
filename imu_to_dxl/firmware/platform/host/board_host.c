#include "board.h"
#include <stdio.h>
#include <string.h>
#include <time.h>

static uint8_t g_rx_q[256];
static unsigned g_rx_r, g_rx_w;
static uint8_t g_last_tx[128];
static size_t g_last_tx_len;
static uint32_t g_ms;

void board_init(void)
{
    g_rx_r = g_rx_w = 0;
    g_last_tx_len = 0;
    g_ms = 0;
}

void board_delay_ms(uint32_t ms)
{
    g_ms += ms;
}

uint32_t board_millis(void)
{
    return g_ms;
}

void board_dxl_set_tx(bool drive_bus)
{
    (void)drive_bus;
}

void board_dxl_write(const uint8_t *data, size_t len)
{
    if (len > sizeof(g_last_tx)) {
        len = sizeof(g_last_tx);
    }
    memcpy(g_last_tx, data, len);
    g_last_tx_len = len;
}

bool board_dxl_read_byte(uint8_t *out)
{
    if (g_rx_r == g_rx_w) {
        return false;
    }
    *out = g_rx_q[g_rx_r++ & 255u];
    return true;
}

/* Test helpers */
void host_dxl_feed(const uint8_t *data, size_t len)
{
    for (size_t i = 0; i < len; i++) {
        g_rx_q[g_rx_w++ & 255u] = data[i];
    }
}

size_t host_dxl_last_tx(uint8_t *out, size_t max)
{
    size_t n = g_last_tx_len < max ? g_last_tx_len : max;
    memcpy(out, g_last_tx, n);
    return n;
}

void host_dxl_clear_tx(void)
{
    g_last_tx_len = 0;
}

/* Fake IMU SPI: WHO_AM_I + zeros */
static uint8_t g_who = 0x70;

int32_t board_imu_spi_write(void *user, uint8_t reg, const uint8_t *data, uint16_t len)
{
    (void)user;
    (void)reg;
    (void)data;
    (void)len;
    return 0;
}

int32_t board_imu_spi_read(void *user, uint8_t reg, uint8_t *data, uint16_t len)
{
    (void)user;
    memset(data, 0, len);
    if (reg == 0x0Fu && len >= 1) {
        data[0] = g_who;
    }
    return 0;
}
