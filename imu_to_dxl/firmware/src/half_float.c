#include "half_float.h"
#include <math.h>

uint16_t md_float_to_half(float f)
{
    union {
        float f;
        uint32_t u;
    } v;
    v.f = f;
    uint32_t x = v.u;
    uint32_t sign = (x >> 16) & 0x8000u;
    int32_t exp = (int32_t)((x >> 23) & 0xFFu) - 127 + 15;
    uint32_t mant = x & 0x7FFFFFu;

    if ((x & 0x7FFFFFFFu) == 0u) {
        return (uint16_t)sign;
    }
    if (exp <= 0) {
        if (exp < -10) {
            return (uint16_t)sign;
        }
        mant |= 0x800000u;
        uint32_t t = (uint32_t)(14 - exp);
        uint32_t half = mant >> (t + 13);
        if ((mant >> (t + 12)) & 1u) {
            half += 1u;
        }
        return (uint16_t)(sign | half);
    }
    if (exp >= 0x1F) {
        return (uint16_t)(sign | 0x7C00u); /* Inf */
    }
    uint16_t half = (uint16_t)(sign | ((uint32_t)exp << 10) | (mant >> 13));
    if (mant & 0x1000u) {
        half = (uint16_t)(half + 1u);
    }
    return half;
}

float md_half_to_float(uint16_t h)
{
    uint32_t sign = (uint32_t)(h & 0x8000u) << 16;
    uint32_t exp = (h >> 10) & 0x1Fu;
    uint32_t mant = h & 0x3FFu;
    uint32_t out;
    if (exp == 0) {
        if (mant == 0) {
            out = sign;
        } else {
            exp = 1;
            while ((mant & 0x400u) == 0u) {
                mant <<= 1;
                exp--;
            }
            mant &= 0x3FFu;
            out = sign | ((exp + (127 - 15)) << 23) | (mant << 13);
        }
    } else if (exp == 0x1F) {
        out = sign | 0x7F800000u | (mant << 13);
    } else {
        out = sign | ((exp + (127 - 15)) << 23) | (mant << 13);
    }
    union {
        uint32_t u;
        float f;
    } v;
    v.u = out;
    return v.f;
}
