#include "dxl_crc.h"
#include "dxl_slave.h"
#include "half_float.h"
#include "imu_pack.h"
#include "control_table.h"
#include "board.h"
#include "host_test.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

static int g_fail;

static void expect(int cond, const char *msg)
{
    if (!cond) {
        printf("FAIL: %s\n", msg);
        g_fail++;
    } else {
        printf("ok: %s\n", msg);
    }
}

static void test_half(void)
{
    uint16_t h = md_float_to_half(1.0f);
    expect(h == 0x3C00u, "half(1.0)==0x3C00");
    float f = md_half_to_float(0x3C00u);
    expect(fabsf(f - 1.0f) < 1e-3f, "half decode 1.0");
}

static void test_pack(void)
{
    md_imu_sample_t s;
    uint8_t b[12];
    memset(&s, 0, sizeof(s));
    s.gyro_raw[0] = 100;
    s.gyro_raw[1] = -200;
    s.gyro_raw[2] = 300;
    s.quat_half[0] = 0x3C00;
    s.quat_half[1] = 0;
    s.quat_half[2] = 0;
    md_imu_pack12(&s, b);
    expect(b[0] == 100 && b[1] == 0, "gyro x le");
    expect((int16_t)(b[2] | (b[3] << 8)) == -200, "gyro y le");
    expect(b[6] == 0x00 && b[7] == 0x3C, "quat x half le");
}

static void build_ping(uint8_t *pkt, uint16_t *len, uint8_t id)
{
    pkt[0] = 0xFF;
    pkt[1] = 0xFF;
    pkt[2] = 0xFD;
    pkt[3] = 0x00;
    pkt[4] = id;
    pkt[5] = 0x03;
    pkt[6] = 0x00;
    pkt[7] = 0x01; /* ping */
    uint16_t crc = md_dxl_crc16(pkt, 8);
    pkt[8] = (uint8_t)(crc & 0xFF);
    pkt[9] = (uint8_t)(crc >> 8);
    *len = 10;
}

static void build_read(uint8_t *pkt, uint16_t *len, uint8_t id, uint16_t addr, uint16_t rlen)
{
    pkt[0] = 0xFF;
    pkt[1] = 0xFF;
    pkt[2] = 0xFD;
    pkt[3] = 0x00;
    pkt[4] = id;
    pkt[5] = 0x07;
    pkt[6] = 0x00;
    pkt[7] = 0x02;
    pkt[8] = (uint8_t)(addr & 0xFF);
    pkt[9] = (uint8_t)(addr >> 8);
    pkt[10] = (uint8_t)(rlen & 0xFF);
    pkt[11] = (uint8_t)(rlen >> 8);
    uint16_t crc = md_dxl_crc16(pkt, 12);
    pkt[12] = (uint8_t)(crc & 0xFF);
    pkt[13] = (uint8_t)(crc >> 8);
    *len = 14;
}

static void test_dxl_ping_read(void)
{
    md_control_table_t table;
    md_dxl_slave_t slave;
    md_imu_sample_t sample;
    uint8_t pkt[32];
    uint16_t plen;
    uint8_t tx[64];
    size_t tlen;

    board_init();
    md_control_table_init(&table);
    memset(&sample, 0, sizeof(sample));
    sample.gyro_raw[0] = 1;
    sample.quat_half[0] = 0x3C00;
    md_control_table_update_imu(&table, &sample);

    md_dxl_slave_init(&slave, 200, table.bytes, MD_CTRL_TABLE_SIZE,
                      board_dxl_set_tx, board_dxl_write);

    host_dxl_clear_tx();
    build_ping(pkt, &plen, 200);
    for (uint16_t i = 0; i < plen; i++) {
        md_dxl_slave_on_byte(&slave, pkt[i]);
    }
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    expect(tlen >= 11 && tx[4] == 200 && tx[7] == 0x55, "ping status");

    host_dxl_clear_tx();
    build_read(pkt, &plen, 200, 124, 12);
    for (uint16_t i = 0; i < plen; i++) {
        md_dxl_slave_on_byte(&slave, pkt[i]);
    }
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    expect(tlen >= 23, "read status len");
    expect(tx[9] == 1 && tx[10] == 0, "read gyro x in params"); /* err at [8], data at [9..] */
    expect(tx[15] == 0x00 && tx[16] == 0x3C, "read quat half");
}

int main(void)
{
    g_fail = 0;
    test_half();
    test_pack();
    test_dxl_ping_read();
    if (g_fail) {
        printf("%d failure(s)\n", g_fail);
        return 1;
    }
    printf("all tests passed\n");
    return 0;
}
