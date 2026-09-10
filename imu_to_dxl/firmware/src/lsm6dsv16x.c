#include "lsm6dsv16x.h"
#include <string.h>

/* Register map (subset) — LSM6DSV16X datasheet / STdC */
#define REG_FUNC_CFG_ACCESS   0x01u
#define REG_FIFO_CTRL1        0x07u
#define REG_FIFO_CTRL3        0x09u
#define REG_FIFO_CTRL4        0x0Au
#define REG_WHO_AM_I          0x0Fu
#define REG_CTRL1_XL          0x10u
#define REG_CTRL2_G           0x11u
#define REG_CTRL3_C           0x12u
#define REG_OUTX_L_G          0x22u
#define REG_OUTX_L_A          0x28u
#define REG_FIFO_STATUS1      0x1Bu
#define REG_FIFO_STATUS2      0x1Cu
#define REG_FIFO_DATA_OUT_TAG 0x78u

#define WHO_AM_I_VAL          0x70u

#define EMB_FUNC_EN_A         0x04u
#define EMB_FUNC_FIFO_EN_A    0x44u
#define SFLP_ODR              0x5Eu
#define EMB_FUNC_INIT_A       0x66u

#define TAG_SFLP_GAME         0x13u
#define FUNC_CFG_ACCESS_EN    0x80u

static int32_t wr(md_lsm6_t *d, uint8_t reg, uint8_t v)
{
    return d->write(d->user, reg, &v, 1);
}

static int32_t rd(md_lsm6_t *d, uint8_t reg, uint8_t *v, uint16_t n)
{
    return d->read(d->user, reg, v, n);
}

static void emb_enter(md_lsm6_t *d)
{
    wr(d, REG_FUNC_CFG_ACCESS, FUNC_CFG_ACCESS_EN);
}

static void emb_exit(md_lsm6_t *d)
{
    wr(d, REG_FUNC_CFG_ACCESS, 0x00u);
}

bool md_lsm6_init(md_lsm6_t *dev)
{
    uint8_t id = 0;
    memset(&dev->last, 0, sizeof(dev->last));
    dev->present = false;
    dev->sflp_live = false;
    dev->sample_count = 0;

    if (!dev->write || !dev->read || !dev->delay_ms) {
        return false;
    }

    dev->delay_ms(15);
    if (rd(dev, REG_WHO_AM_I, &id, 1) != 0 || id != WHO_AM_I_VAL) {
        return false;
    }
    dev->present = true;
    dev->last.status = 0x01u;

    wr(dev, REG_CTRL3_C, 0x44u); /* BDU=1, IF_INC=1 */
    dev->delay_ms(5);

    /* LSM6DSV16X: ODR in CTRL1/CTRL2; FS_G in CTRL6 (not classic LSM6DSR layout). */
    wr(dev, REG_CTRL1_XL, 0x05u); /* ODR_XL = 60 Hz */
    wr(dev, REG_CTRL2_G, 0x05u);  /* ODR_G = 60 Hz */
    wr(dev, 0x15u, 0x02u);        /* CTRL6: FS_G = ±500 dps */
    wr(dev, 0x17u, 0x01u);        /* CTRL8: FS_XL = ±4 g (bits1:0=01) */

    wr(dev, REG_FIFO_CTRL1, 0x10u);
    wr(dev, REG_FIFO_CTRL3, 0x00u);
    wr(dev, REG_FIFO_CTRL4, 0x06u); /* continuous */

    emb_enter(dev);
    wr(dev, EMB_FUNC_EN_A, 0x02u);      /* SFLP_GAME_EN */
    wr(dev, EMB_FUNC_FIFO_EN_A, 0x01u); /* game rotation → FIFO */
    wr(dev, SFLP_ODR, 0x03u);           /* ~60 Hz class */
    wr(dev, EMB_FUNC_INIT_A, 0x08u);    /* SFLP_GAME_INIT */
    emb_exit(dev);

    return true;
}

static void read_gyro_accel(md_lsm6_t *dev)
{
    uint8_t raw[12];
    if (rd(dev, REG_OUTX_L_G, raw, 6) != 0) {
        return;
    }
    if (rd(dev, REG_OUTX_L_A, &raw[6], 6) != 0) {
        return;
    }
    dev->last.gyro_raw[0] = (int16_t)(raw[0] | ((uint16_t)raw[1] << 8));
    dev->last.gyro_raw[1] = (int16_t)(raw[2] | ((uint16_t)raw[3] << 8));
    dev->last.gyro_raw[2] = (int16_t)(raw[4] | ((uint16_t)raw[5] << 8));
    dev->last.accel_raw[0] = (int16_t)(raw[6] | ((uint16_t)raw[7] << 8));
    dev->last.accel_raw[1] = (int16_t)(raw[8] | ((uint16_t)raw[9] << 8));
    dev->last.accel_raw[2] = (int16_t)(raw[10] | ((uint16_t)raw[11] << 8));
}

bool md_lsm6_poll(md_lsm6_t *dev)
{
    uint8_t st1 = 0, st2 = 0;
    uint16_t level;
    uint16_t drained = 0;

    if (!dev->present) {
        return false;
    }

    read_gyro_accel(dev);

    if (rd(dev, REG_FIFO_STATUS1, &st1, 1) != 0) {
        return false;
    }
    (void)rd(dev, REG_FIFO_STATUS2, &st2, 1);
    level = (uint16_t)(st1 | (((uint16_t)st2 & 0x01u) << 8));

    while (level > 0u && drained < 48u) {
        uint8_t slot[7];
        uint8_t tag_lo;
        if (rd(dev, REG_FIFO_DATA_OUT_TAG, slot, 7) != 0) {
            break;
        }
        tag_lo = (uint8_t)(slot[0] & 0x1Fu);
        if (tag_lo == TAG_SFLP_GAME) {
            dev->last.quat_half[0] = (uint16_t)(slot[1] | ((uint16_t)slot[2] << 8));
            dev->last.quat_half[1] = (uint16_t)(slot[3] | ((uint16_t)slot[4] << 8));
            dev->last.quat_half[2] = (uint16_t)(slot[5] | ((uint16_t)slot[6] << 8));
            if (dev->last.quat_half[0] | dev->last.quat_half[1] | dev->last.quat_half[2]) {
                dev->sflp_live = true;
            }
        }
        level--;
        drained++;
    }

    if (!dev->sflp_live) {
        dev->last.quat_half[0] = 0;
        dev->last.quat_half[1] = 0;
        dev->last.quat_half[2] = 0;
    }

    /* Bump counter every poll so host stale-tracker sees life even before SFLP. */
    dev->sample_count = (uint16_t)(dev->sample_count + 1u);
    /* Fold a low nibble of counter into unused gyro LSBs? No — keep gyro clean.
       Host compares full 12B; gyro noise + changing quat is enough. For silent gyro,
       XOR sample into a reserved path: we rely on gyro raw changing or quat. */
    if (!dev->sflp_live && (dev->sample_count & 1u)) {
        /* Toggle unused high bit of gyro_z LSB area safely? Better: leave as-is.
           Stale detection before motion: sample_count is only in diag @136. */
    }

    dev->last.sample_count = dev->sample_count;
    dev->last.status = (uint8_t)(0x01u | (dev->sflp_live ? 0x02u : 0x00u));
    return true;
}
