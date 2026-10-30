/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#pragma once

namespace blender::ed::sculpt_paint::spinner {

/* Returns true if the Rust 1€ path ran and wrote r_mouse. False = use C++ path. */
bool stroke_smooth_1euro(const float2 &mouse, float2 &r_mouse);

}  // namespace blender::ed::sculpt_paint::spinner
