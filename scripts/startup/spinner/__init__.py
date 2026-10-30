# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D startup package
# Loaded by Blender's startup system.

def register():
    from . import hardsurface
    from . import workspace
    hardsurface.register()
    workspace.register()

def unregister():
    from . import hardsurface
    from . import workspace
    hardsurface.unregister()
    workspace.unregister()
