#include "dxl_crc.h"
#include "dxl_slave.h"
#include "half_float.h"
#include "imu_pack.h"
#include "lsm6dsv16x.h"
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

typedef struct {
    uint8_t main_regs[256];
    uint8_t emb_regs[256];
    uint8_t embedded;
    uint8_t fifo_slot[7];
} fake_imu_t;

static int32_t fake_imu_write(void *user, uint8_t reg, const uint8_t *data, uint16_t len)
{
    fake_imu_t *f = (fake_imu_t *)user;
    if (reg == 0x01u && len == 1u) {
        f->embedded = (uint8_t)((data[0] & 0x80u) != 0u);
        return 0;
    }
    memcpy(&(f->embedded ? f->emb_regs : f->main_regs)[reg], data, len);
    return 0;
}

static int32_t fake_imu_read(void *user, uint8_t reg, uint8_t *data, uint16_t len)
{
    fake_imu_t *f = (fake_imu_t *)user;
    if (!f->embedded && reg == 0x78u && len == 7u) {
        memcpy(data, f->fifo_slot, 7u);
        f->main_regs[0x1Bu] = 0u;
        return 0;
    }
    memcpy(data, &(f->embedded ? f->emb_regs : f->main_regs)[reg], len);
    return 0;
}

static void fake_delay(uint32_t ms) { (void)ms; }

static void test_sflp_configuration_and_tag(void)
{
    fake_imu_t f;
    md_lsm6_t imu;
    memset(&f, 0, sizeof(f));
    memset(&imu, 0, sizeof(imu));
    f.main_regs[0x0Fu] = 0x70u;
    imu.user = &f; imu.write = fake_imu_write; imu.read = fake_imu_read; imu.delay_ms = fake_delay;
    expect(md_lsm6_init(&imu), "SFLP init with register readback");
    expect((f.emb_regs[0x04] & 0x02u) != 0u, "SFLP game enable bit1");
    expect((f.emb_regs[0x44] & 0x02u) != 0u, "SFLP game FIFO enable bit1");
    expect((f.emb_regs[0x5E] & 0x38u) == 0x10u, "SFLP 60Hz ODR in bits5:3");
    expect((f.emb_regs[0x66] & 0x02u) != 0u, "SFLP init bit1");

    f.main_regs[0x1Bu] = 1u;
    f.fifo_slot[0] = (uint8_t)(0x13u << 3);
    f.fifo_slot[1] = 0x00u; f.fifo_slot[2] = 0x3Cu;
    expect(md_lsm6_poll(&imu) && imu.sflp_live && imu.last.quat_half[0] == 0x3C00u,
           "FIFO tag decodes from bits7:3");
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

static void build_packet(uint8_t *pkt, uint16_t *len, uint8_t id,
                         const uint8_t *body, uint16_t body_len)
{
    uint8_t stuffed[96];
    uint16_t sn = 0;
    for (uint16_t i = 0; i < body_len; i++) {
        stuffed[sn++] = body[i];
        if (i >= 2u && body[i - 2u] == 0xFFu && body[i - 1u] == 0xFFu &&
            body[i] == 0xFDu) {
            stuffed[sn++] = 0xFDu;
        }
    }
    pkt[0] = 0xFFu; pkt[1] = 0xFFu; pkt[2] = 0xFDu; pkt[3] = 0;
    pkt[4] = id;
    uint16_t wire_len = (uint16_t)(sn + 2u);
    pkt[5] = (uint8_t)wire_len; pkt[6] = (uint8_t)(wire_len >> 8);
    memcpy(&pkt[7], stuffed, sn);
    uint16_t crc = md_dxl_crc16(pkt, (uint16_t)(7u + sn));
    pkt[7u + sn] = (uint8_t)crc;
    pkt[8u + sn] = (uint8_t)(crc >> 8);
    *len = (uint16_t)(9u + sn);
}

static void feed(md_dxl_slave_t *s, const uint8_t *pkt, uint16_t len)
{
    for (uint16_t i = 0; i < len; i++) {
        md_dxl_slave_on_byte(s, pkt[i]);
    }
}

static int status_crc_ok(const uint8_t *pkt, size_t n)
{
    if (n < 10u) return 0;
    uint16_t got = (uint16_t)(pkt[n - 2u] | ((uint16_t)pkt[n - 1u] << 8));
    return md_dxl_crc16(pkt, (uint16_t)(n - 2u)) == got;
}

static void test_dxl_robustness(void)
{
    md_control_table_t table;
    md_dxl_slave_t slave;
    uint8_t pkt[128], tx[192];
    uint16_t plen;
    size_t tlen;
    board_init();
    md_control_table_init(&table);
    md_dxl_slave_init(&slave, 200, table.bytes, MD_CTRL_TABLE_SIZE,
                      board_dxl_set_tx, board_dxl_write);

    uint8_t sync[] = {0x82u, 124u, 0, 12u, 0, 200u, 1u};
    build_packet(pkt, &plen, 0xFEu, sync, sizeof(sync));
    host_dxl_clear_tx(); feed(&slave, pkt, plen);
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    expect(tlen > 0u && tx[7] == 0x55u && status_crc_ok(tx, tlen), "sync_read ID200 first");

    uint8_t read_oob[] = {0x02u, 150u, 0, 8u, 0};
    build_packet(pkt, &plen, 200u, read_oob, sizeof(read_oob));
    host_dxl_clear_tx(); feed(&slave, pkt, plen);
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    expect(tlen == 11u && tx[8] == 0x04u, "overlong read returns data range");

    uint8_t write_oob[] = {0x03u, 151u, 0, 1u, 2u};
    build_packet(pkt, &plen, 200u, write_oob, sizeof(write_oob));
    host_dxl_clear_tx(); feed(&slave, pkt, plen);
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    expect(tlen == 11u && tx[8] == 0x04u, "overlong write returns data range");

    table.bytes[124] = 0xFFu; table.bytes[125] = 0xFFu; table.bytes[126] = 0xFDu;
    build_read(pkt, &plen, 200u, 124u, 12u);
    host_dxl_clear_tx(); feed(&slave, pkt, plen);
    tlen = host_dxl_last_tx(tx, sizeof(tx));
    int found = 0;
    for (size_t i = 7; i + 3 < tlen; i++) {
        if (tx[i] == 0xFFu && tx[i+1] == 0xFFu && tx[i+2] == 0xFDu && tx[i+3] == 0xFDu) found = 1;
    }
    expect(found && status_crc_ok(tx, tlen), "status stuffs FF FF FD and CRC covers wire packet");

    uint8_t stuffed_write[] = {0x03u, 20u, 0, 0xFFu, 0xFFu, 0xFDu};
    build_packet(pkt, &plen, 200u, stuffed_write, sizeof(stuffed_write));
    host_dxl_clear_tx(); feed(&slave, pkt, plen);
    expect(table.bytes[20] == 0xFFu && table.bytes[21] == 0xFFu && table.bytes[22] == 0xFDu,
           "RX unstuffing preserves write payload");

    expect(host_dxl_tx_transitions() == 2u && !host_dxl_is_driving(),
           "TX direction returns to RX without self-listen state");
}

int main(void)
{
    g_fail = 0;
    test_half();
    test_sflp_configuration_and_tag();
    test_pack();
    test_dxl_ping_read();
    test_dxl_robustness();
    if (g_fail) {
        printf("%d failure(s)\n", g_fail);
        return 1;
    }
    printf("all tests passed\n");
    return 0;
}
