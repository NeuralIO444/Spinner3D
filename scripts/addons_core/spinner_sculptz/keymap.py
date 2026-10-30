# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z keymap
# Applied only while the Sculpt Z workspace is active.

import bpy

addon_keymaps = []


def register_keymap():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc is None:
        return

    km = kc.keymaps.new(name="Sculpt", space_type="EMPTY")

    # Ctrl mask, Ctrl-Alt unmask
    kmi = km.keymap_items.new("sculpt.brush_stroke", "LEFTMOUSE", "PRESS", ctrl=True)
    kmi.properties.mode = "NORMAL"
    addon_keymaps.append((km, kmi))

    # Alt invert (handled by brush; placeholder for future)
    # Shift smooth
    kmi = km.keymap_items.new("sculpt.brush_stroke", "LEFTMOUSE", "PRESS", shift=True)
    addon_keymaps.append((km, kmi))

    # S / U / O for size / strength / falloff (radial control)
    kmi = km.keymap_items.new("spinner_sculptz.radial_size", "S", "PRESS")
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new("spinner_sculptz.radial_strength", "U", "PRESS")
    addon_keymaps.append((km, kmi))

    # D / Shift-D for subdiv levels
    kmi = km.keymap_items.new("spinner_sculptz.subdiv_up", "D", "PRESS")
    addon_keymaps.append((km, kmi))
    kmi = km.keymap_items.new("spinner_sculptz.subdiv_down", "D", "PRESS", shift=True)
    addon_keymaps.append((km, kmi))

    # B + letter brush picks (examples)
    kmi = km.keymap_items.new("spinner_sculptz.apply_brush", "B", "PRESS", ctrl=True)
    addon_keymaps.append((km, kmi))

    # Empty-space navigation
    kmi = km.keymap_items.new("spinner_sculptz.navigate", "LEFTMOUSE", "PRESS")
    addon_keymaps.append((km, kmi))

    # Spacebar palette
    kmi = km.keymap_items.new("spinner_sculptz.palette", "SPACE", "PRESS")
    addon_keymaps.append((km, kmi))


def unregister_keymap():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def register():
    register_keymap()


def unregister():
    unregister_keymap()
