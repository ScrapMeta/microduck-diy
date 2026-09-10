/**
 * STM32G031F8 — board bring-up for imu_to_dxl_ref **v0.3**.
 * Pin map: docs/hardware.md (USART2 + SPI1 + PA1 OE#; PA0 INT input).
 * No Cube HAL. CMSIS device header optional when linking full image.
 */
#include "board.h"
#include "md_config.h"
#include <stddef.h>

#if defined(MD_PLATFORM_STM32G031)

#include <stdint.h>
#include <stdbool.h>

#define PERIPH_BASE        0x40000000u
#define AHBPERIPH_BASE     (PERIPH_BASE + 0x00020000u)
#define RCC_BASE           (AHBPERIPH_BASE + 0x00001000u)
#define GPIOA_BASE         (AHBPERIPH_BASE + 0x00000000u)

#define APBPERIPH_BASE     PERIPH_BASE
#define USART2_BASE        (APBPERIPH_BASE + 0x00004400u)
#define SPI1_BASE          (APBPERIPH_BASE + 0x00013000u)

#define RCC_IOPENR         (*(volatile uint32_t *)(RCC_BASE + 0x34u))
#define RCC_APBENR1        (*(volatile uint32_t *)(RCC_BASE + 0x3Cu))
#define RCC_APBENR2        (*(volatile uint32_t *)(RCC_BASE + 0x40u))
#define RCC_CFGR           (*(volatile uint32_t *)(RCC_BASE + 0x08u))
#define RCC_CR             (*(volatile uint32_t *)(RCC_BASE + 0x00u))

#define GPIOA_MODER        (*(volatile uint32_t *)(GPIOA_BASE + 0x00u))
#define GPIOA_OTYPER       (*(volatile uint32_t *)(GPIOA_BASE + 0x04u))
#define GPIOA_OSPEEDR      (*(volatile uint32_t *)(GPIOA_BASE + 0x08u))
#define GPIOA_PUPDR        (*(volatile uint32_t *)(GPIOA_BASE + 0x0Cu))
#define GPIOA_IDR          (*(volatile uint32_t *)(GPIOA_BASE + 0x10u))
#define GPIOA_ODR          (*(volatile uint32_t *)(GPIOA_BASE + 0x14u))
#define GPIOA_BSRR         (*(volatile uint32_t *)(GPIOA_BASE + 0x18u))
#define GPIOA_AFRL         (*(volatile uint32_t *)(GPIOA_BASE + 0x20u))
#define GPIOA_AFRH         (*(volatile uint32_t *)(GPIOA_BASE + 0x24u))

#define USART_CR1          (*(volatile uint32_t *)(USART2_BASE + 0x00u))
#define USART_CR2          (*(volatile uint32_t *)(USART2_BASE + 0x04u))
#define USART_CR3          (*(volatile uint32_t *)(USART2_BASE + 0x08u))
#define USART_BRR          (*(volatile uint32_t *)(USART2_BASE + 0x0Cu))
#define USART_ISR          (*(volatile uint32_t *)(USART2_BASE + 0x1Cu))
#define USART_ICR          (*(volatile uint32_t *)(USART2_BASE + 0x20u))
#define USART_RDR          (*(volatile uint32_t *)(USART2_BASE + 0x24u))
#define USART_TDR          (*(volatile uint32_t *)(USART2_BASE + 0x28u))

#define SPI_CR1            (*(volatile uint32_t *)(SPI1_BASE + 0x00u))
#define SPI_CR2            (*(volatile uint32_t *)(SPI1_BASE + 0x04u))
#define SPI_SR             (*(volatile uint32_t *)(SPI1_BASE + 0x08u))
#define SPI_DR             (*(volatile uint32_t *)(SPI1_BASE + 0x0Cu))

#define PIN_MODER(pin, mode) \
    do { \
        GPIOA_MODER = (GPIOA_MODER & ~(3u << ((pin) * 2))) | ((uint32_t)(mode) << ((pin) * 2)); \
    } while (0)

static volatile uint32_t g_ms;

void SysTick_Handler(void)
{
    g_ms++;
}

static void clock_init_bringup(void)
{
    /* HSI 16 MHz SYSCLK for bring-up; BRR = 16 → 1 Mbps on USART2. */
    (void)RCC_CR;
    (void)RCC_CFGR;
}

static void gpio_init(void)
{
    RCC_IOPENR |= (1u << 0); /* GPIOA */

    /* PA0 IMU_INT — input floating (SFLP path is polled; INT reserved) */
    PIN_MODER(MD_PIN_IMU_INT, 0);

    /* PA1 OE# output; idle high = RX (bus high-Z) */
    PIN_MODER(MD_PIN_DXL_OE, 1);
    GPIOA_BSRR = (1u << MD_PIN_DXL_OE);

    /* PA4 CS output high */
    PIN_MODER(MD_PIN_SPI_CS, 1);
    GPIOA_BSRR = (1u << MD_PIN_SPI_CS);

    /* PA2/PA3 AF1 USART2 (DXL half-duplex via 1G125) */
    PIN_MODER(MD_PIN_USART2_TX, 2);
    PIN_MODER(MD_PIN_USART2_RX, 2);
    GPIOA_AFRL = (GPIOA_AFRL & ~(0xFFu << (MD_PIN_USART2_TX * 4))) |
                 (0x11u << (MD_PIN_USART2_TX * 4)); /* AF1, AF1 */

    /* PA5/6/7 AF0 SPI1 → LSM6 */
    PIN_MODER(MD_PIN_SPI_SCK, 2);
    PIN_MODER(MD_PIN_SPI_MISO, 2);
    PIN_MODER(MD_PIN_SPI_MOSI, 2);
    GPIOA_AFRL &= ~((0xFul << (MD_PIN_SPI_SCK * 4)) |
                    (0xFul << (MD_PIN_SPI_MISO * 4)) |
                    (0xFul << (MD_PIN_SPI_MOSI * 4)));
    GPIOA_OSPEEDR |= (3u << (MD_PIN_SPI_SCK * 2)) | (3u << (MD_PIN_SPI_MOSI * 2));

    /*
     * PA11/PA12 = USART1 on J2 BM07 (v0.3 debug). Left as reset/input;
     * enable only when a console is needed (avoids AF clash with unused path).
     * SWD PA13/PA14 owned by debugger — do not reconfigure here.
     */
    (void)MD_PIN_USART1_TX;
    (void)MD_PIN_USART1_RX;
    (void)MD_PIN_SWDIO;
    (void)MD_PIN_SWCLK;
}

static void usart2_init(void)
{
    RCC_APBENR1 |= (1u << 17); /* USART2EN */
    USART_CR1 = 0;
    USART_BRR = 16; /* 16 MHz / MD_IMU_BAUD */
    USART_CR1 = (1u << 3) | (1u << 2) | (1u << 0); /* TE RE UE */
}

static void spi1_init(void)
{
    RCC_APBENR2 |= (1u << 12); /* SPI1EN */
    SPI_CR1 = 0;
    /* Master, SSM/SSI, BR/8, CPOL0 CPHA0 */
    SPI_CR1 = (1u << 2) | (1u << 8) | (1u << 9) | (2u << 3);
    SPI_CR2 = (7u << 8); /* DS=8bit */
    SPI_CR1 |= (1u << 6); /* SPE */
}

static uint8_t spi_xfer(uint8_t v)
{
    while ((SPI_SR & (1u << 1)) == 0) {
    }
    *(volatile uint8_t *)&SPI_DR = v;
    while ((SPI_SR & (1u << 0)) == 0) {
    }
    return *(volatile uint8_t *)&SPI_DR;
}

void board_init(void)
{
    clock_init_bringup();
    gpio_init();
    usart2_init();
    spi1_init();
    /* SysTick 1 ms at 16 MHz */
    *(volatile uint32_t *)0xE000E014u = 16000u - 1u;
    *(volatile uint32_t *)0xE000E010u = 7u;
    g_ms = 0;
}

void board_delay_ms(uint32_t ms)
{
    uint32_t start = g_ms;
    while ((g_ms - start) < ms) {
    }
}

uint32_t board_millis(void)
{
    return g_ms;
}

void board_dxl_set_tx(bool drive_bus)
{
    if (drive_bus) {
        GPIOA_BSRR = (1u << (MD_PIN_DXL_OE + 16)); /* OE# low = TX */
    } else {
        GPIOA_BSRR = (1u << MD_PIN_DXL_OE); /* OE# high = RX */
    }
}

void board_dxl_write(const uint8_t *data, size_t len)
{
    for (size_t i = 0; i < len; i++) {
        while ((USART_ISR & (1u << 7)) == 0) {
        }
        USART_TDR = data[i];
    }
    while ((USART_ISR & (1u << 6)) == 0) {
    } /* TC */
}

bool board_dxl_read_byte(uint8_t *out)
{
    if (USART_ISR & (1u << 5)) {
        *out = (uint8_t)USART_RDR;
        return true;
    }
    return false;
}

int32_t board_imu_spi_write(void *user, uint8_t reg, const uint8_t *data, uint16_t len)
{
    (void)user;
    GPIOA_BSRR = (1u << (MD_PIN_SPI_CS + 16)); /* CS low */
    (void)spi_xfer(reg & 0x7Fu);
    for (uint16_t i = 0; i < len; i++) {
        (void)spi_xfer(data[i]);
    }
    GPIOA_BSRR = (1u << MD_PIN_SPI_CS); /* CS high */
    return 0;
}

int32_t board_imu_spi_read(void *user, uint8_t reg, uint8_t *data, uint16_t len)
{
    (void)user;
    GPIOA_BSRR = (1u << (MD_PIN_SPI_CS + 16));
    (void)spi_xfer((uint8_t)(reg | 0x80u));
    for (uint16_t i = 0; i < len; i++) {
        data[i] = spi_xfer(0xFFu);
    }
    GPIOA_BSRR = (1u << MD_PIN_SPI_CS);
    return 0;
}

#else
/* Non-G031 translation unit placeholder — host platform supplies board_*. */
#endif
