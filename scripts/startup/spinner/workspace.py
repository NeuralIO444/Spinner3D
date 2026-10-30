# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Hard Surface workspace preset
# Creates a workspace with matcap + cavity, wireframe overlay, and hard-surface snapping.

import bpy
from bpy.types import Operator
from bpy.app.handlers import persistent


WORKSPACE_NAME = "Hard Surface"


def ensure_hard_surface_workspace():
    """Create the Hard Surface workspace if missing and configure the active 3D view."""
    wm = bpy.context.window_manager
    if not wm.windows:
        return None

    win = wm.windows[0]
    # Duplicate Layout if Hard Surface doesn't exist
    if WORKSPACE_NAME not in bpy.data.workspaces:
        # Prefer duplicating Modeling or Layout
        source = None
        for name in ("Modeling", "Layout"):
            if name in bpy.data.workspaces:
                source = bpy.data.workspaces[name]
                break
        if source is None:
            source = bpy.data.workspaces[0]
        # Use operator via override
        with bpy.context.temp_override(window=win, workspace=source):
            bpy.ops.workspace.duplicate()
        # The new workspace is the active one
        new_ws = win.workspace
        new_ws.name = WORKSPACE_NAME
    else:
        new_ws = bpy.data.workspaces[WORKSPACE_NAME]

    # Configure 3D viewport overlays in the active screen
    for area in win.screen.areas:
        if area.type != "VIEW_3D":
            continue
        space = area.spaces.active
        # Shading
        space.shading.type = "SOLID"
        space.shading.light = "MATCAP"
        space.shading.show_cavity = True
        space.shading.cavity_type = "BOTH"
        # Overlays
        space.overlay.show_overlays = True
        space.overlay.show_wireframes = True
        space.overlay.wireframe_threshold = 0.8
        # Snapping
        tool = space.context_tool_settings if hasattr(space, "context_tool_settings") else bpy.context.scene.tool_settings
        ts = bpy.context.scene.tool_settings
        ts.use_snap = True
        ts.snap_elements = {"VERTEX", "EDGE", "MIDPOINT"}
        ts.use_snap_align_rotation = True
        break
    return new_ws


class SPINNER3D_OT_hard_surface_workspace(Operator):
    """Switch to or create the Hard Surface workspace"""
    bl_idname = "spinner3d.hard_surface_workspace"
    bl_label = "Hard Surface Workspace"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ws = ensure_hard_surface_workspace()
        if ws is None:
            self.report({"WARNING"}, "No window available")
            return {"CANCELLED"}
        context.window.workspace = ws
        self.report({"INFO"}, f"Switched to {WORKSPACE_NAME}")
        return {"FINISHED"}


@persistent
def load_handler(_):
    # Create workspace on factory startup if missing
    if WORKSPACE_NAME not in bpy.data.workspaces:
        ensure_hard_surface_workspace()


classes = (SPINNER3D_OT_hard_surface_workspace,)



def menu_func(self, context):
    self.layout.operator(SPINNER3D_OT_hard_surface_workspace.bl_idname, icon="WORKSPACE")


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_view.append(menu_func)
    bpy.app.handlers.load_factory_startup_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
    bpy.types.VIEW3D_MT_view.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
