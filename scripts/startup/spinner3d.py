# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D entry point. Auto-loaded by Blender startup.

import importlib

def register():
    try:
        import spinner
        importlib.reload(spinner)
        spinner.register()
    except Exception as ex:
        print(f"Spinner3D startup failed: {ex}")

def unregister():
    try:
        import spinner
        spinner.unregister()
    except Exception:
        pass

register()
