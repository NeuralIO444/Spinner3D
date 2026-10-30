# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z keymap
# Items are added only while the Sculpt Z workspace is active
# and removed on exit so they do not leak to other workspaces.

import bpy
from bpy.app.handlers import persistent

addon_keymaps = []
_active = False

WORKSPACE_NAME = "Sculpt Z"


def _is_sculptz():
    wm = bpy.context.window_manager
    if not wm.windows:
        return False
    return wm.windows[0].workspace.name == WORKSPACE_NAME


def _add_keymap():
    global _active
    if _active:
        return
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        return

    km = kc.keymaps.new(name="Sculpt", space_type="EMPTY")

    items = [
        ("spinner_sculptz.navigate", "LEFTMOUSE", "PRESS", {}),
        ("spinner_sculptz.radial_size", "S", "PRESS", {}),
        ("spinner_sculptz.radial_strength", "U", "PRESS", {}),
        ("spinner_sculptz.subdiv_up", "D", "PRESS", {}),
        ("spinner_sculptz.subdiv_down", "D", "PRESS", {"shift": True}),
        ("spinner_sculptz.palette", "SPACE", "PRESS", {}),
        ("sculpt.brush_stroke", "LEFTMOUSE", "PRESS", {"ctrl": True}),
        ("sculpt.brush_stroke", "LEFTMOUSE", "PRESS", {"shift": True}),
    ]

    for idname, key, value, kwargs in items:
        kmi = km.keymap_items.new(idname, key, value, **kwargs)
        addon_keymaps.append((km, kmi))

    _active = True


def _remove_keymap():
    global _active
    if not _active:
        return
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass
    addon_keymaps.clear()
    _active = False


@persistent
def on_depsgraph(_):
    """Toggle keymap based on active workspace."""
    if _is_sculptz():
        _add_keymap()
    else:
        _remove_keymap()


def register():
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph)
    # Initial check
    if _is_sculptz():
        _add_keymap()


def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph)
    _remove_keymap()
