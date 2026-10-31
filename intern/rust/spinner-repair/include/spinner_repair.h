#ifndef SPINNER_REPAIR_H
#define SPINNER_REPAIR_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint64_t spinner_repair_create(uint8_t fill_holes, uint8_t fix_non_manifold);
int32_t spinner_repair_free(uint64_t id);
int32_t spinner_repair_will_fill_holes(uint64_t id);

#ifdef __cplusplus
}
#endif

#endif
