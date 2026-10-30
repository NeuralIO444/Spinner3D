# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z workspace addon
# Phase 1: one-click ZBrush-feel sculpting workspace

bl_info = {
    "name": "Spinner3D Sculpt Z",
    "author": "Spinner3D",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Workspace > Sculpt Z",
    "description": "ZBrush-feel sculpting workspace: keymap, shelf, brush pack, Dynamesh-style remesh",
    "category": "Sculpt",
}

import bpy
from bpy.app.handlers import persistent

from . import keymap
from . import operators
from . import shelf
from . import workspace
from . import navigate
from . import popup


@persistent
def on_workspace_change(_):
    """Restore or apply Sculpt Z keymap based on active workspace."""
    workspace.on_workspace_changed()


def register():
    operators.register()
    shelf.register()
    navigate.register()
    popup.register()
    keymap.register()
    workspace.register()
    bpy.app.handlers.depsgraph_update_post.append(on_workspace_change)


def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(on_workspace_change)
    workspace.unregister()
    keymap.unregister()
    popup.unregister()
    navigate.unregister()
    shelf.unregister()
    operators.unregister()
