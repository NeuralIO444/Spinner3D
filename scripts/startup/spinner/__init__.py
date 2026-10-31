# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D startup package
# Loaded by Blender's startup system.

def register():
    from . import hardsurface
    from . import workspace
    from . import instant_meshes
    hardsurface.register()
    workspace.register()
    instant_meshes.register()

def unregister():
    from . import hardsurface
    from . import workspace
    from . import instant_meshes
    hardsurface.unregister()
    workspace.unregister()
    instant_meshes.unregister()
