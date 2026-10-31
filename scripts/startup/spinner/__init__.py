# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D startup package
# Loaded by Blender's startup system.

def register():
    from . import hardsurface
    hardsurface.register()

def unregister():
    from . import hardsurface
    hardsurface.unregister()
