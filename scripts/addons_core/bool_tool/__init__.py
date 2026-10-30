# SPDX-License-Identifier: GPL-3.0-or-later
# Bundled by Spinner3D. Upstream: https://github.com/nickberckley/bool_tool
bl_info = {
    "name": "Bool Tool",
    "author": "nickberckley",
    "version": (2, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Edit",
    "description": "Boolean operations and cutter management",
    "category": "Object",
}

if "bpy" in locals():
    import importlib
    for mod in [operators,
                tools,
                ui,
                manual,
                preferences,
                properties,
                ]:
        importlib.reload(mod)
    print("Add-on Reloaded: Bool Tool")
else:
    import bpy
    from . import (
        operators,
        tools,
        ui,
        manual,
        preferences,
        properties,
    )


#### ------------------------------ REGISTRATION ------------------------------ ####

modules = (
    operators,
    tools,
    ui,
    manual,
    preferences,
    properties,
)

def register():
    for module in modules:
        module.register()

    preferences.update_sidebar_category(bpy.context.preferences.addons[__package__].preferences, bpy.context)


def unregister():
    for module in reversed(modules):
        module.unregister()
