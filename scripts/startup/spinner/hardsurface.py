# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D hard-surface stack operator
# Placed in scripts/startup/spinner/ so it loads with the build.

bl_info = {
    "name": "Spinner3D Hard Surface",
    "author": "Spinner3D",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Object > Hard Surface Stack / Toolbar",
    "description": "Idempotent Bevel + Weighted Normal + Smooth by Angle stack",
    "category": "Object",
}

import bpy
from bpy.types import Operator, Menu
from bpy.props import FloatProperty, IntProperty


STACK_NAME = "Spinner3D_HS"


def get_or_create_modifier(obj, mod_type, name_suffix):
    """Return existing modifier of the given type in the stack, or create it."""
    full_name = f"{STACK_NAME}_{name_suffix}"
    for mod in obj.modifiers:
        if mod.name == full_name and mod.type == mod_type:
            return mod
    mod = obj.modifiers.new(name=full_name, type=mod_type)
    return mod


class SPINNER3D_OT_hard_surface_stack(Operator):
    """Add or update Bevel (angle) + Weighted Normal + Smooth by Angle"""
    bl_idname = "spinner3d.hard_surface_stack"
    bl_label = "Hard Surface Stack"
    bl_options = {"REGISTER", "UNDO"}

    bevel_width: FloatProperty(name="Bevel Width", default=0.01, min=0.0, max=1.0)
    bevel_segments: IntProperty(name="Bevel Segments", default=2, min=1, max=8)
    bevel_angle: FloatProperty(name="Bevel Angle", default=0.5236, min=0.0, max=3.1416)  # ~30 deg

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active mesh required")
            return {"CANCELLED"}

        # Bevel (angle limit, harden normals)
        bevel = get_or_create_modifier(obj, "BEVEL", "Bevel")
        bevel.width = self.bevel_width
        bevel.segments = self.bevel_segments
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = self.bevel_angle
        bevel.harden_normals = True
        bevel.use_clamp_overlap = True

        # Weighted Normal
        wn = get_or_create_modifier(obj, "WEIGHTED_NORMAL", "WeightedNormal")
        wn.keep_sharp = True
        wn.weight = 50

        # Smooth by Angle
        smooth = get_or_create_modifier(obj, "SMOOTH", "SmoothByAngle")
        # Smooth modifier does not have angle; use the dedicated Smooth by Angle if available
        # Fall back to regular Smooth with low factor for compatibility
        smooth.factor = 0.5
        smooth.iterations = 1

        # Try to use the dedicated Smooth by Angle modifier if present in this Blender version
        try:
            sba = get_or_create_modifier(obj, "SMOOTH_BY_ANGLE", "SmoothByAngle")
            sba.angle = self.bevel_angle
            # Remove the generic Smooth if we successfully created the better one
            if smooth != sba:
                obj.modifiers.remove(smooth)
        except Exception:
            pass

        self.report({"INFO"}, "Hard Surface stack updated")
        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(SPINNER3D_OT_hard_surface_stack.bl_idname, text="Hard Surface Stack")


def register():
    bpy.utils.register_class(SPINNER3D_OT_hard_surface_stack)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(SPINNER3D_OT_hard_surface_stack)


if __name__ == "__main__":
    register()
