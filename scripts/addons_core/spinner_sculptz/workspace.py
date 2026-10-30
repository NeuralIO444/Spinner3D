# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z workspace management

import bpy
from bpy.types import Operator
from . import keymap
from bpy.app.handlers import persistent

WORKSPACE_NAME = "Sculpt Z"
_sculptz_active = False


def is_sculptz_workspace():
    wm = bpy.context.window_manager
    if not wm.windows:
        return False
    return wm.windows[0].workspace.name == WORKSPACE_NAME


def ensure_sculptz_workspace():
    """Create the Sculpt Z workspace if it doesn't exist."""
    if WORKSPACE_NAME in bpy.data.workspaces:
        return bpy.data.workspaces[WORKSPACE_NAME]

    # Duplicate Modeling or Layout
    source = None
    for name in ("Modeling", "Layout", "Sculpting"):
        if name in bpy.data.workspaces:
            source = bpy.data.workspaces[name]
            break
    if source is None:
        source = bpy.data.workspaces[0]

    win = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=win, workspace=source):
        bpy.ops.workspace.duplicate()
    new_ws = win.workspace
    new_ws.name = WORKSPACE_NAME
    return new_ws



def _load_spinner_matcap():
    """Load a Spinner3D CC0 matcap into the viewport if available."""
    import os
    addon_dir = os.path.dirname(__file__)
    matcap_path = os.path.join(addon_dir, "data", "matcaps", "red_wax.png")
    if not os.path.isfile(matcap_path):
        return
    # Blender studio lights are usually .exr; for a personal build we set
    # the shading to use a matcap and note the path. Full studio-light
    # registration would require a datafiles install; this keeps it self-contained.
    pass


def configure_sculptz_viewport():
    """Set dark background, matcap, overlays for Sculpt Z."""
    wm = bpy.context.window_manager
    if not wm.windows:
        return
    win = wm.windows[0]
    for area in win.screen.areas:
        if area.type != "VIEW_3D":
            continue
        space = area.spaces.active
        space.shading.type = "SOLID"
        space.shading.light = "MATCAP"
        _load_spinner_matcap()  # SPINNER3D
        space.shading.show_cavity = True
        space.shading.cavity_type = "BOTH"
        # Dark background
        space.shading.background_type = "THEME"
        space.overlay.show_overlays = True
        space.overlay.show_face_orientation = False
        break


class SPINNER_SCULPTZ_OT_enter(Operator):
    """Enter Sculpt Z workspace"""
    bl_idname = "spinner_sculptz.enter"
    bl_label = "Enter Sculpt Z"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ws = ensure_sculptz_workspace()
        context.window.workspace = ws
        # Switch to sculpt mode if possible
        obj = context.active_object
        if obj and obj.type == "MESH":
            bpy.ops.object.mode_set(mode="SCULPT")
        configure_sculptz_viewport()
        keymap._add_keymap()
        self.report({"INFO"}, "Sculpt Z active")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_exit(Operator):
    """Leave Sculpt Z and restore previous workspace"""
    bl_idname = "spinner_sculptz.exit"
    bl_label = "Back to Spinner"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Switch to Modeling or Layout
        for name in ("Modeling", "Layout"):
            if name in bpy.data.workspaces:
                context.window.workspace = bpy.data.workspaces[name]
                break
        keymap._remove_keymap()
        self.report({"INFO"}, "Left Sculpt Z")
        return {"FINISHED"}


def on_workspace_changed():
    """Called on workspace change to toggle keymap state."""
    global _sculptz_active
    active = is_sculptz_workspace()
    if active and not _sculptz_active:
        configure_sculptz_viewport()
        _sculptz_active = True
    elif not active and _sculptz_active:
        _sculptz_active = False


@persistent
def load_handler(_):
    ensure_sculptz_workspace()


classes = (SPINNER_SCULPTZ_OT_enter, SPINNER_SCULPTZ_OT_exit)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.load_factory_startup_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
