# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z radial popup and spacebar palette stubs

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, EnumProperty


class SPINNER_SCULPTZ_OT_radial_size(Operator):
    """Radial size control at cursor"""
    bl_idname = "spinner_sculptz.radial_size"
    bl_label = "Brush Size"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.mode != "SCULPT":
            return {"CANCELLED"}
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",
            data_path_primary="tool_settings.sculpt.brush.size",
        )
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_radial_strength(Operator):
    """Radial strength control at cursor"""
    bl_idname = "spinner_sculptz.radial_strength"
    bl_label = "Brush Strength"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.mode != "SCULPT":
            return {"CANCELLED"}
        bpy.ops.wm.radial_control(
            "INVOKE_DEFAULT",
            data_path_primary="tool_settings.sculpt.brush.strength",
        )
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_palette(Operator):
    """Spacebar brush palette at cursor"""
    bl_idname = "spinner_sculptz.palette"
    bl_label = "Brush Palette"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        if context.mode != "SCULPT":
            return {"CANCELLED"}
        # Use a simple popup menu of brush presets
        bpy.ops.wm.call_menu(name="SPINNER_SCULPTZ_MT_palette")
        return {"FINISHED"}


class SPINNER_SCULPTZ_MT_palette(bpy.types.Menu):
    bl_label = "Brushes"
    bl_idname = "SPINNER_SCULPTZ_MT_palette"

    def draw(self, context):
        layout = self.layout
        for name in ("Move", "ClayBuildup", "DamStandard", "hPolish", "TrimDynamic", "Inflate", "Standard", "Pinch", "SnakeHook"):
            op = layout.operator("spinner_sculptz.apply_brush", text=name)
            op.brush_name = name


classes = (
    SPINNER_SCULPTZ_OT_radial_size,
    SPINNER_SCULPTZ_OT_radial_strength,
    SPINNER_SCULPTZ_OT_palette,
    SPINNER_SCULPTZ_MT_palette,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
