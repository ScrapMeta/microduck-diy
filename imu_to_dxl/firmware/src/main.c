#include "board.h"
#include "control_table.h"
#include "dxl_slave.h"
#include "lsm6dsv16x.h"
#include "md_config.h"

static md_control_table_t g_table;
static md_dxl_slave_t g_dxl;
static md_lsm6_t g_imu;

int main(void)
{
    board_init();
    md_control_table_init(&g_table);

    md_dxl_slave_init(&g_dxl,
                      MD_IMU_DXL_ID,
                      g_table.bytes,
                      MD_CTRL_TABLE_SIZE,
                      board_dxl_set_tx,
                      board_dxl_write);

    g_imu.user = 0;
    g_imu.write = board_imu_spi_write;
    g_imu.read = board_imu_spi_read;
    g_imu.delay_ms = board_delay_ms;
    if (!md_lsm6_init(&g_imu)) {
        /* Keep DXL alive and expose probe/config failure at diagnostics @136. */
        md_control_table_update_imu(&g_table, &g_imu.last);
    }

    uint32_t last_sample = 0;
    for (;;) {
        uint8_t b;
        while (board_dxl_read_byte(&b)) {
            md_dxl_slave_on_byte(&g_dxl, b);
        }

        uint32_t now = board_millis();
        if ((now - last_sample) >= 10u) { /* ~100 Hz sample / 50 Hz host ok */
            last_sample = now;
            if (md_lsm6_poll(&g_imu)) {
                md_control_table_update_imu(&g_table, &g_imu.last);
            }
        }
    }
}
