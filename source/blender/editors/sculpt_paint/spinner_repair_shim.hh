/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#pragma once

#include <cstdint>

namespace blender::ed::sculpt_paint::spinner {

uint64_t repair_create(uint8_t fill_holes, uint8_t fix_non_manifold);
int repair_will_fill_holes(uint64_t id);
int repair_free(uint64_t id);

}  // namespace blender::ed::sculpt_paint::spinner
