#include "dxl_slave.h"
#include "dxl_crc.h"
#include <string.h>

enum {
    ST_IDLE = 0,
    ST_FF,
    ST_FF2,
    ST_FD,
    ST_RSV,
    ST_ID,
    ST_LEN_L,
    ST_LEN_H,
    ST_PAYLOAD
};

#define INST_PING       0x01u
#define INST_READ       0x02u
#define INST_WRITE      0x03u
#define INST_SYNC_READ  0x82u
#define INST_STATUS     0x55u

static void send_status(md_dxl_slave_t *s, uint8_t err, const uint8_t *params, uint16_t n)
{
    uint8_t pkt[80];
    uint16_t len = (uint16_t)(3u + n); /* inst + err + params + later replaced: length = inst..crc-2 */
    /* Protocol 2 status: length = bytes from instruction through params, then CRC adds 2 outside length? 
     * Spec: Length = number of bytes from Instruction to CRC16 (exclusive of CRC) =  Instruction(1) + Error(1) + Params(N) + ... wait
     * Actually: Length field = Instruction + parameters + CRC(2)  i.e. N+3 for status with N params? 
     * Robotis: Length = the length of the packet from Instruction field to CRC16 field (inclusive of CRC?).
     * Official: Length = Parameter length + 3 (Instruction + Error + CRC low? No)
     * From e-manual: Length = number of bytes of Instruction + Parameters + CRC fields.
     * Status: Instruction(1) + Error(1) + Params(N) + CRC(2) ⇒ Length = N + 4
     */
    uint16_t length = (uint16_t)(n + 4u);
    uint16_t i = 0;
    pkt[i++] = 0xFF;
    pkt[i++] = 0xFF;
    pkt[i++] = 0xFD;
    pkt[i++] = 0x00;
    pkt[i++] = s->id;
    pkt[i++] = (uint8_t)(length & 0xFF);
    pkt[i++] = (uint8_t)((length >> 8) & 0xFF);
    pkt[i++] = INST_STATUS;
    pkt[i++] = err;
    if (n && params) {
        memcpy(&pkt[i], params, n);
        i = (uint16_t)(i + n);
    }
    uint16_t crc = md_dxl_crc16(pkt, i);
    pkt[i++] = (uint8_t)(crc & 0xFF);
    pkt[i++] = (uint8_t)((crc >> 8) & 0xFF);

    if (s->set_tx) {
        s->set_tx(true);
    }
    if (s->write_bytes) {
        s->write_bytes(pkt, i);
    }
    if (s->set_tx) {
        s->set_tx(false);
    }
}

static void handle_read(md_dxl_slave_t *s, uint16_t addr, uint16_t len)
{
    if (addr >= s->table_size) {
        send_status(s, 0x07, NULL, 0); /* access range */
        return;
    }
    if ((uint32_t)addr + len > s->table_size) {
        len = (uint16_t)(s->table_size - addr);
    }
    send_status(s, 0x00, &s->table[addr], len);
}

static void handle_write(md_dxl_slave_t *s, uint16_t addr, const uint8_t *data, uint16_t len)
{
    /* Allow only return delay (9) and a small scratch region for bring-up. */
    for (uint16_t i = 0; i < len; i++) {
        uint16_t a = (uint16_t)(addr + i);
        if (a == 9u || (a >= 20u && a < 30u)) {
            s->table[a] = data[i];
        }
    }
    send_status(s, 0x00, NULL, 0);
}

static void handle_sync_read(md_dxl_slave_t *s, const uint8_t *p, uint16_t n)
{
    if (n < 4u) {
        return;
    }
    uint16_t addr = (uint16_t)(p[0] | ((uint16_t)p[1] << 8));
    uint16_t len = (uint16_t)(p[2] | ((uint16_t)p[3] << 8));
    /* IDs start at p[4] */
    for (uint16_t i = 4; i < n; i++) {
        if (p[i] == s->id) {
            /* Host lists IMU first — respond immediately. */
            handle_read(s, addr, len);
            return;
        }
    }
}

static void handle_packet(md_dxl_slave_t *s)
{
    /* rx: FF FF FD 00 ID LEN_L LEN_H INST PARAM... CRC_L CRC_H */
    if (s->rx_len < 10u) {
        return;
    }
    uint8_t id = s->rx[4];
    uint16_t length = (uint16_t)(s->rx[5] | ((uint16_t)s->rx[6] << 8));
    uint16_t total = (uint16_t)(7u + length);
    if (s->rx_len < total) {
        return;
    }
    uint16_t crc_calc = md_dxl_crc16(s->rx, (uint16_t)(total - 2u));
    uint16_t crc_rx = (uint16_t)(s->rx[total - 2u] | ((uint16_t)s->rx[total - 1u] << 8));
    if (crc_calc != crc_rx) {
        return;
    }
    uint8_t inst = s->rx[7];
    const uint8_t *params = &s->rx[8];
    uint16_t plen = (uint16_t)(length - 3u); /* inst + crc(2) excluded from remaining params */
    if (length < 3u) {
        return;
    }

    if (id != s->id && id != 0xFEu && inst != INST_SYNC_READ) {
        return;
    }

    switch (inst) {
    case INST_PING:
        if (id == s->id || id == 0xFEu) {
            send_status(s, 0x00, NULL, 0);
        }
        break;
    case INST_READ:
        if (id == s->id && plen >= 4u) {
            uint16_t addr = (uint16_t)(params[0] | ((uint16_t)params[1] << 8));
            uint16_t rlen = (uint16_t)(params[2] | ((uint16_t)params[3] << 8));
            handle_read(s, addr, rlen);
        }
        break;
    case INST_WRITE:
        if (id == s->id && plen >= 2u) {
            uint16_t addr = (uint16_t)(params[0] | ((uint16_t)params[1] << 8));
            handle_write(s, addr, &params[2], (uint16_t)(plen - 2u));
        }
        break;
    case INST_SYNC_READ:
        handle_sync_read(s, params, plen);
        break;
    default:
        break;
    }
}

void md_dxl_slave_init(md_dxl_slave_t *s,
                       uint8_t id,
                       uint8_t *table,
                       uint16_t table_size,
                       md_dxl_set_tx_fn set_tx,
                       md_dxl_write_bytes_fn write_bytes)
{
    memset(s, 0, sizeof(*s));
    s->id = id;
    s->table = table;
    s->table_size = table_size;
    s->set_tx = set_tx;
    s->write_bytes = write_bytes;
    s->state = ST_IDLE;
    if (s->set_tx) {
        s->set_tx(false);
    }
}

void md_dxl_slave_on_byte(md_dxl_slave_t *s, uint8_t b)
{
    switch (s->state) {
    case ST_IDLE:
        if (b == 0xFFu) {
            s->rx[0] = b;
            s->rx_len = 1;
            s->state = ST_FF;
        }
        break;
    case ST_FF:
        if (b == 0xFFu) {
            s->rx[1] = b;
            s->rx_len = 2;
            s->state = ST_FF2;
        } else {
            s->state = ST_IDLE;
        }
        break;
    case ST_FF2:
        if (b == 0xFDu) {
            s->rx[2] = b;
            s->rx_len = 3;
            s->state = ST_FD;
        } else if (b == 0xFFu) {
            /* stay */
        } else {
            s->state = ST_IDLE;
        }
        break;
    case ST_FD:
        if (b == 0x00u) {
            s->rx[3] = b;
            s->rx_len = 4;
            s->state = ST_ID;
        } else {
            s->state = ST_IDLE;
        }
        break;
    case ST_ID:
        s->rx[4] = b;
        s->rx_len = 5;
        s->state = ST_LEN_L;
        break;
    case ST_LEN_L:
        s->rx[5] = b;
        s->rx_len = 6;
        s->state = ST_LEN_H;
        break;
    case ST_LEN_H:
        s->rx[6] = b;
        s->rx_len = 7;
        s->expect_len = (uint16_t)(s->rx[5] | ((uint16_t)s->rx[6] << 8));
        if (s->expect_len < 3u || s->expect_len > 50u) {
            s->state = ST_IDLE;
            break;
        }
        s->state = ST_PAYLOAD;
        break;
    case ST_PAYLOAD:
        if (s->rx_len < sizeof(s->rx)) {
            s->rx[s->rx_len++] = b;
        }
        if (s->rx_len >= (uint16_t)(7u + s->expect_len)) {
            handle_packet(s);
            s->state = ST_IDLE;
            s->rx_len = 0;
        }
        break;
    default:
        s->state = ST_IDLE;
        break;
    }
}
