#include "dxl_slave.h"
#include "dxl_crc.h"
#include <string.h>

#define INST_PING       0x01u
#define INST_READ       0x02u
#define INST_WRITE      0x03u
#define INST_SYNC_READ  0x82u
#define INST_STATUS     0x55u

#define DXL_ERR_INSTRUCTION 0x02u
#define DXL_ERR_DATA_RANGE  0x04u
#define DXL_ERR_DATA_LENGTH 0x05u
#define DXL_ERR_ACCESS      0x07u
#define DXL_HEADER_SIZE     7u
#define DXL_CRC_SIZE        2u
#define DXL_STATUS_FIXED    2u
#define DXL_MAX_PARAMS      80u

static uint16_t stuff_body(const uint8_t *src, uint16_t n, uint8_t *dst, uint16_t cap)
{
    uint16_t out = 0;
    for (uint16_t i = 0; i < n; i++) {
        if (out >= cap) {
            return 0;
        }
        dst[out++] = src[i];
        if (i >= 2u && src[i - 2u] == 0xFFu && src[i - 1u] == 0xFFu &&
            src[i] == 0xFDu) {
            if (out >= cap) {
                return 0;
            }
            dst[out++] = 0xFDu;
        }
    }
    return out;
}

static uint16_t unstuff_body(const uint8_t *src, uint16_t n, uint8_t *dst, uint16_t cap)
{
    uint16_t out = 0;
    for (uint16_t i = 0; i < n; i++) {
        if (out >= cap) {
            return 0;
        }
        dst[out++] = src[i];
        if (out >= 3u && dst[out - 3u] == 0xFFu && dst[out - 2u] == 0xFFu &&
            dst[out - 1u] == 0xFDu && i + 1u < n && src[i + 1u] == 0xFDu) {
            i++;
        }
    }
    return out;
}

static void send_status(md_dxl_slave_t *s, uint8_t err, const uint8_t *params, uint16_t n)
{
    uint8_t body[DXL_STATUS_FIXED + DXL_MAX_PARAMS];
    uint8_t stuffed[sizeof(body) + sizeof(body) / 3u + 1u];
    uint8_t pkt[DXL_HEADER_SIZE + sizeof(stuffed) + DXL_CRC_SIZE];
    uint16_t stuffed_n;
    uint16_t length;
    uint16_t i = 0;

    if (n > DXL_MAX_PARAMS) {
        err = DXL_ERR_DATA_LENGTH;
        params = NULL;
        n = 0;
    }
    body[0] = INST_STATUS;
    body[1] = err;
    if (n != 0u && params != NULL) {
        memcpy(&body[2], params, n);
    }
    stuffed_n = stuff_body(body, (uint16_t)(DXL_STATUS_FIXED + n), stuffed,
                           (uint16_t)sizeof(stuffed));
    if (stuffed_n == 0u) {
        return;
    }
    length = (uint16_t)(stuffed_n + DXL_CRC_SIZE);
    pkt[i++] = 0xFFu;
    pkt[i++] = 0xFFu;
    pkt[i++] = 0xFDu;
    pkt[i++] = 0x00u;
    pkt[i++] = s->id;
    pkt[i++] = (uint8_t)length;
    pkt[i++] = (uint8_t)(length >> 8);
    memcpy(&pkt[i], stuffed, stuffed_n);
    i = (uint16_t)(i + stuffed_n);
    uint16_t crc = md_dxl_crc16(pkt, i);
    pkt[i++] = (uint8_t)crc;
    pkt[i++] = (uint8_t)(crc >> 8);

    if (s->set_tx != NULL) {
        s->set_tx(true);
    }
    if (s->write_bytes != NULL) {
        s->write_bytes(pkt, i);
    }
    if (s->set_tx != NULL) {
        s->set_tx(false);
    }
}

static void handle_read(md_dxl_slave_t *s, uint16_t addr, uint16_t len)
{
    if (addr >= s->table_size || (uint32_t)addr + len > s->table_size) {
        send_status(s, DXL_ERR_DATA_RANGE, NULL, 0);
    } else if (len > DXL_MAX_PARAMS) {
        send_status(s, DXL_ERR_DATA_LENGTH, NULL, 0);
    } else {
        send_status(s, 0, &s->table[addr], len);
    }
}

static void handle_write(md_dxl_slave_t *s, uint16_t addr, const uint8_t *data, uint16_t len)
{
    if (addr >= s->table_size || (uint32_t)addr + len > s->table_size) {
        send_status(s, DXL_ERR_DATA_RANGE, NULL, 0);
        return;
    }
    for (uint16_t i = 0; i < len; i++) {
        uint16_t a = (uint16_t)(addr + i);
        if (a != 9u && !(a >= 20u && a < 30u)) {
            send_status(s, DXL_ERR_ACCESS, NULL, 0);
            return;
        }
    }
    for (uint16_t i = 0; i < len; i++) {
        s->table[addr + i] = data[i];
    }
    send_status(s, 0, NULL, 0);
}

static void handle_sync_read(md_dxl_slave_t *s, const uint8_t *p, uint16_t n)
{
    if (n < 5u) {
        return;
    }
    uint16_t addr = (uint16_t)(p[0] | ((uint16_t)p[1] << 8));
    uint16_t len = (uint16_t)(p[2] | ((uint16_t)p[3] << 8));
    for (uint16_t i = 4; i < n; i++) {
        if (p[i] == s->id) {
            handle_read(s, addr, len);
            return;
        }
    }
}

static void handle_packet(md_dxl_slave_t *s)
{
    uint16_t length = (uint16_t)(s->rx[5] | ((uint16_t)s->rx[6] << 8));
    uint16_t total = (uint16_t)(DXL_HEADER_SIZE + length);
    uint16_t crc_rx;
    uint8_t body[sizeof(s->rx)];
    uint16_t body_len;

    if (length < 3u || total != s->rx_len) {
        return;
    }
    crc_rx = (uint16_t)(s->rx[total - 2u] | ((uint16_t)s->rx[total - 1u] << 8));
    if (md_dxl_crc16(s->rx, (uint16_t)(total - 2u)) != crc_rx) {
        return;
    }
    body_len = unstuff_body(&s->rx[7], (uint16_t)(length - 2u), body,
                            (uint16_t)sizeof(body));
    if (body_len == 0u) {
        return;
    }
    uint8_t id = s->rx[4];
    uint8_t inst = body[0];
    const uint8_t *params = &body[1];
    uint16_t plen = (uint16_t)(body_len - 1u);

    if (id != s->id && id != 0xFEu && inst != INST_SYNC_READ) {
        return;
    }
    switch (inst) {
    case INST_PING:
        if (id == s->id || id == 0xFEu) {
            uint8_t info[3] = {s->table[0], s->table[1], s->table[2]};
            send_status(s, 0, info, sizeof(info));
        }
        break;
    case INST_READ:
        if (id == s->id && plen == 4u) {
            handle_read(s, (uint16_t)(params[0] | ((uint16_t)params[1] << 8)),
                        (uint16_t)(params[2] | ((uint16_t)params[3] << 8)));
        } else if (id == s->id) {
            send_status(s, DXL_ERR_DATA_LENGTH, NULL, 0);
        }
        break;
    case INST_WRITE:
        if (id == s->id && plen >= 3u) {
            handle_write(s, (uint16_t)(params[0] | ((uint16_t)params[1] << 8)),
                         &params[2], (uint16_t)(plen - 2u));
        } else if (id == s->id) {
            send_status(s, DXL_ERR_DATA_LENGTH, NULL, 0);
        }
        break;
    case INST_SYNC_READ:
        if (id == 0xFEu) {
            handle_sync_read(s, params, plen);
        }
        break;
    default:
        if (id == s->id) {
            send_status(s, DXL_ERR_INSTRUCTION, NULL, 0);
        }
        break;
    }
}

void md_dxl_slave_init(md_dxl_slave_t *s, uint8_t id, uint8_t *table,
                       uint16_t table_size, md_dxl_set_tx_fn set_tx,
                       md_dxl_write_bytes_fn write_bytes)
{
    memset(s, 0, sizeof(*s));
    s->id = id;
    s->table = table;
    s->table_size = table_size;
    s->set_tx = set_tx;
    s->write_bytes = write_bytes;
    if (set_tx != NULL) {
        set_tx(false);
    }
}

void md_dxl_slave_on_byte(md_dxl_slave_t *s, uint8_t b)
{
    if (s->rx_len == 0u) {
        if (b == 0xFFu) {
            s->rx[s->rx_len++] = b;
        }
        return;
    }
    if ((s->rx_len == 1u && b != 0xFFu) ||
        (s->rx_len == 2u && b != 0xFDu) ||
        (s->rx_len == 3u && b != 0x00u)) {
        s->rx_len = (b == 0xFFu) ? 1u : 0u;
        s->rx[0] = b;
        return;
    }
    if (s->rx_len >= sizeof(s->rx)) {
        s->rx_len = 0;
        return;
    }
    s->rx[s->rx_len++] = b;
    if (s->rx_len == DXL_HEADER_SIZE) {
        s->expect_len = (uint16_t)(s->rx[5] | ((uint16_t)s->rx[6] << 8));
        if (s->expect_len < 3u || s->expect_len > sizeof(s->rx) - DXL_HEADER_SIZE) {
            s->rx_len = 0;
        }
    } else if (s->rx_len >= DXL_HEADER_SIZE &&
               s->rx_len == (uint16_t)(DXL_HEADER_SIZE + s->expect_len)) {
        handle_packet(s);
        s->rx_len = 0;
    }
}
