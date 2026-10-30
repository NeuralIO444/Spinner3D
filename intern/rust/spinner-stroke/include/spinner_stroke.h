#ifndef SPINNER_STROKE_H
#define SPINNER_STROKE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

int32_t spinner_stroke_smooth_1euro(const float *points, uint32_t len, float cutoff, float beta, float *out);

#ifdef __cplusplus
}
#endif

#endif
