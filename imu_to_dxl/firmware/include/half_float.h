#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/** IEEE754 binary16 encode (round-to-nearest-even). */
uint16_t md_float_to_half(float f);

/** Decode binary16 → float (host-side / tests). */
float md_half_to_float(uint16_t h);

#ifdef __cplusplus
}
#endif
