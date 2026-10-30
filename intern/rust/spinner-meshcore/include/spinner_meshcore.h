#ifndef SPINNER_MESHCORE_H
#define SPINNER_MESHCORE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint64_t spinner_mesh_create(void);
int32_t spinner_mesh_free(uint64_t id);
int32_t spinner_mesh_vert_count(uint64_t id);
int32_t spinner_mesh_add_vert(uint64_t id, float x, float y, float z);

#ifdef __cplusplus
}
#endif

#endif
