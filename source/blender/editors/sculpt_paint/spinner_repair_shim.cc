/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#include "spinner_repair_shim.hh"

#ifdef WITH_SPINNER_RUST_REPAIR
#  include "spinner_repair.h"
#endif

namespace blender::ed::sculpt_paint::spinner {

uint64_t repair_create(uint8_t fill_holes, uint8_t fix_non_manifold)
{
#ifdef WITH_SPINNER_RUST_REPAIR
  return spinner_repair_create(fill_holes, fix_non_manifold);
#else
  (void)fill_holes;
  (void)fix_non_manifold;
  return 0;
#endif
}

int repair_will_fill_holes(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_REPAIR
  return spinner_repair_will_fill_holes(id);
#else
  (void)id;
  return -1;
#endif
}

int repair_free(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_REPAIR
  return spinner_repair_free(id);
#else
  (void)id;
  return -1;
#endif
}

}  // namespace blender::ed::sculpt_paint::spinner
