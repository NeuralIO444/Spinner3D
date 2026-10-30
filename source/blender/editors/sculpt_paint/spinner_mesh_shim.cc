/* SPDX-FileCopyrightText: 2026 Spinner3D Authors */
/* SPDX-License-Identifier: GPL-3.0-or-later */

#include "spinner_mesh_shim.hh"

#ifdef WITH_SPINNER_RUST_MESHCORE
#  include "spinner_meshcore.h"
#endif

namespace blender::ed::sculpt_paint::spinner {

uint64_t mesh_create()
{
#ifdef WITH_SPINNER_RUST_MESHCORE
  return spinner_mesh_create();
#else
  return 0;
#endif
}

int mesh_add_vert(uint64_t id, float x, float y, float z)
{
#ifdef WITH_SPINNER_RUST_MESHCORE
  return spinner_mesh_add_vert(id, x, y, z);
#else
  (void)id;
  (void)x;
  (void)y;
  (void)z;
  return -1;
#endif
}

int mesh_vert_count(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_MESHCORE
  return spinner_mesh_vert_count(id);
#else
  (void)id;
  return -1;
#endif
}

int mesh_free(uint64_t id)
{
#ifdef WITH_SPINNER_RUST_MESHCORE
  return spinner_mesh_free(id);
#else
  (void)id;
  return -1;
#endif
}

}  // namespace blender::ed::sculpt_paint::spinner
