#ifndef SPINNER_REMESH_H
#define SPINNER_REMESH_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint64_t spinner_remesh_create(float target_edge_len, uint32_t iterations);
int32_t spinner_remesh_free(uint64_t id);
int32_t spinner_remesh_iterations(uint64_t id);

#ifdef __cplusplus
}
#endif

#endif
