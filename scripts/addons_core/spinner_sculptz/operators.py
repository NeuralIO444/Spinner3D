# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z operators

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, EnumProperty


# Brush presets tuned from Blender's built-in brushes
BRUSH_PRESETS = {
    "Move": {"sculpt_brush_type": "GRAB", "strength": 0.5, "size": 60},
    "ClayBuildup": {"sculpt_brush_type": "CLAY_STRIPS", "strength": 0.4, "size": 40, "plane_offset": 0.1},
    "DamStandard": {"sculpt_brush_type": "CREASE", "strength": 0.6, "size": 20, "crease_pinch_factor": 0.5},
    "hPolish": {"sculpt_brush_type": "FLATTEN", "strength": 0.3, "size": 50, "plane_offset": 0.0},
    "TrimDynamic": {"sculpt_brush_type": "SCRAPE", "strength": 0.4, "size": 45},
    "Inflate": {"sculpt_brush_type": "INFLATE", "strength": 0.4, "size": 40},
    "Standard": {"sculpt_brush_type": "DRAW", "strength": 0.5, "size": 50},
    "Pinch": {"sculpt_brush_type": "PINCH", "strength": 0.5, "size": 25},
    "SnakeHook": {"sculpt_brush_type": "SNAKE_HOOK", "strength": 0.5, "size": 30},
}


class SPINNER_SCULPTZ_OT_apply_brush(Operator):
    """Apply a Spinner brush preset"""
    bl_idname = "spinner_sculptz.apply_brush"
    bl_label = "Apply Brush"
    bl_options = {"REGISTER", "UNDO"}

    brush_name: EnumProperty(
        name="Brush",
        items=[(k, k, "") for k in BRUSH_PRESETS.keys()],
    )

    def execute(self, context):
        if context.mode != "SCULPT":
            self.report({"WARNING"}, "Sculpt mode required")
            return {"CANCELLED"}
        preset = BRUSH_PRESETS.get(self.brush_name)
        if not preset:
            return {"CANCELLED"}
        brush = context.tool_settings.sculpt.brush
        if brush is None:
            return {"CANCELLED"}
        for key, value in preset.items():
            if hasattr(brush, key):
                setattr(brush, key, value)
        self.report({"INFO"}, f"Brush: {self.brush_name}")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_dynamesh(Operator):
    """Voxel remesh keeping Face Sets (Dynamesh-style)"""
    bl_idname = "spinner_sculptz.dynamesh"
    bl_label = "Dynamesh"
    bl_options = {"REGISTER", "UNDO"}

    voxel_size: FloatProperty(name="Voxel Size", default=0.05, min=0.001, max=1.0)

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active mesh required")
            return {"CANCELLED"}
        # Store face sets if present
        mesh = obj.data
        has_face_sets = "face_set" in mesh.attributes
        # Remesh
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.voxel_remesh(voxel_size=self.voxel_size)
        # Face sets are preserved by Blender's voxel remesh when possible
        bpy.ops.object.mode_set(mode="SCULPT")
        self.report({"INFO"}, f"Remeshed (voxel {self.voxel_size:.3f})")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_subdiv_up(Operator):
    """Increase Multires subdivision level"""
    bl_idname = "spinner_sculptz.subdiv_up"
    bl_label = "Subdiv Up"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {"CANCELLED"}
        for mod in obj.modifiers:
            if mod.type == "MULTIRES":
                mod.levels += 1
                self.report({"INFO"}, f"Level {mod.levels}")
                return {"FINISHED"}
        self.report({"WARNING"}, "No Multires modifier")
        return {"CANCELLED"}


class SPINNER_SCULPTZ_OT_subdiv_down(Operator):
    """Decrease Multires subdivision level"""
    bl_idname = "spinner_sculptz.subdiv_down"
    bl_label = "Subdiv Down"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            return {"CANCELLED"}
        for mod in obj.modifiers:
            if mod.type == "MULTIRES" and mod.levels > 0:
                mod.levels -= 1
                self.report({"INFO"}, f"Level {mod.levels}")
                return {"FINISHED"}
        self.report({"WARNING"}, "No Multires or already at 0")
        return {"CANCELLED"}


class SPINNER_SCULPTZ_OT_isolate(Operator):
    """Isolate active Face Set"""
    bl_idname = "spinner_sculptz.isolate"
    bl_label = "Isolate"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.mode != "SCULPT":
            return {"CANCELLED"}
        bpy.ops.sculpt.face_set_change_visibility(mode="TOGGLE")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_show_all(Operator):
    """Show all Face Sets"""
    bl_idname = "spinner_sculptz.show_all"
    bl_label = "Show All"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.mode != "SCULPT":
            return {"CANCELLED"}
        bpy.ops.sculpt.face_set_change_visibility(mode="SHOW_ALL")
        return {"FINISHED"}


classes = (
    SPINNER_SCULPTZ_OT_apply_brush,
    SPINNER_SCULPTZ_OT_dynamesh,
    SPINNER_SCULPTZ_OT_subdiv_up,
    SPINNER_SCULPTZ_OT_subdiv_down,
    SPINNER_SCULPTZ_OT_isolate,
    SPINNER_SCULPTZ_OT_show_all,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
