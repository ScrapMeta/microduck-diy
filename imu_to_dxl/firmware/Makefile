# imu_to_dxl firmware
# host-test: no ARM toolchain required
# TARGET=g031: needs arm-none-eabi-gcc

BUILD ?= build
HOST_CC ?= gcc
CROSS ?= arm-none-eabi-

INCLUDES = -Iinclude -Iplatform/host

HOST_SRCS = \
	src/dxl_crc.c \
	src/half_float.c \
	src/imu_pack.c \
	src/control_table.c \
	src/dxl_slave.c \
	platform/host/board_host.c \
	tests/test_host.c

.PHONY: all host-test clean g031

all: host-test

host-test: $(BUILD)/host_test
	$(BUILD)/host_test

$(BUILD)/host_test: $(HOST_SRCS)
	mkdir -p $(BUILD)
	$(HOST_CC) -std=c11 -Wall -Wextra -O2 $(INCLUDES) $(HOST_SRCS) -lm -o $@

# Minimal G031 image (no Cube). Link with provided startup/linker.
G031_SRCS = \
	src/main.c \
	src/dxl_crc.c \
	src/half_float.c \
	src/imu_pack.c \
	src/control_table.c \
	src/dxl_slave.c \
	src/lsm6dsv16x.c \
	platform/stm32g031/board_g031.c \
	platform/stm32g031/startup_stm32g031xx.s \
	platform/stm32g031/syscalls.c

g031: $(BUILD)/imu_to_dxl.elf

$(BUILD)/imu_to_dxl.elf: $(G031_SRCS) platform/stm32g031/STM32G031F8Px_FLASH.ld
	mkdir -p $(BUILD)
	$(CROSS)gcc -std=c11 -Wall -Wextra -O2 -g \
		-mcpu=cortex-m0plus -mthumb \
		-DMD_PLATFORM_STM32G031 \
		-Iinclude \
		-Tplatform/stm32g031/STM32G031F8Px_FLASH.ld \
		-Wl,--gc-sections -ffunction-sections -fdata-sections \
		$(G031_SRCS) -o $@ -lc -lm -lnosys
	$(CROSS)objcopy -O binary $@ $(BUILD)/imu_to_dxl.bin
	$(CROSS)size $@

clean:
	rm -rf $(BUILD)
