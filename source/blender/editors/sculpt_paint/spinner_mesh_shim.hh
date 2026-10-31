/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#pragma once

#include <cstdint>

namespace blender::ed::sculpt_paint::spinner {

/* Returns a non-zero id on success, 0 on failure or when the flag is off. */
uint64_t mesh_create();
int mesh_add_vert(uint64_t id, float x, float y, float z);
int mesh_vert_count(uint64_t id);
int mesh_free(uint64_t id);

}  // namespace blender::ed::sculpt_paint::spinner
