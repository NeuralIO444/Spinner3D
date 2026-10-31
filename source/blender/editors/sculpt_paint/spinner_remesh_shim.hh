/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#pragma once

#include <cstdint>

namespace blender::ed::sculpt_paint::spinner {

uint64_t remesh_create(float target_edge_len, uint32_t iterations);
int remesh_iterations(uint64_t id);
int remesh_free(uint64_t id);

}  // namespace blender::ed::sculpt_paint::spinner
