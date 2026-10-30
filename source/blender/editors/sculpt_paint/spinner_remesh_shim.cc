/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#include "spinner_remesh_shim.hh"

#ifdef WITH_SPINNER_RUST_REMESH
#  include "spinner_remesh.h"
#endif

namespace blender::ed::sculpt_paint::spinner {

uint64_t remesh_create(float target_edge_len, uint32_t iterations)
{
#ifdef WITH_SPINNER_RUST_REMESH
  return spinner_remesh_create(target_edge_len, iterations);
#else
  (void)target_edge_len;
  (void)iterations;
  return 0;
#endif
}

int remesh_iterations(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_REMESH
  return spinner_remesh_iterations(id);
#else
  (void)id;
  return -1;
#endif
}

int remesh_free(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_REMESH
  return spinner_remesh_free(id);
#else
  (void)id;
  return -1;
#endif
}

}  // namespace blender::ed::sculpt_paint::spinner
