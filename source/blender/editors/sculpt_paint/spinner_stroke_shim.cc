/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#include "spinner_stroke_shim.hh"

#include "BLI_math_vector_types.hh"

#ifdef WITH_SPINNER_RUST_STROKE
#  include "spinner_stroke.h"
#endif

namespace blender::ed::sculpt_paint::spinner {

bool stroke_smooth_1euro(const float2 &mouse, float2 &r_mouse)
{
#ifdef WITH_SPINNER_RUST_STROKE
  float in[2] = {mouse.x, mouse.y};
  float out[2] = {0.0f, 0.0f};
  const int code = spinner_stroke_smooth_1euro(in, 1, 1.0f, 0.0f, out);
  if (code == 0) {
    r_mouse = float2(out[0], out[1]);
    return true;
  }
#endif
  r_mouse = mouse;
  return false;
}

}  // namespace blender::ed::sculpt_paint::spinner
