# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z Phase 2 operators
# Polypaint, sculpt layers, project detail, retopo button.

import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, StringProperty, EnumProperty


class SPINNER_SCULPTZ_OT_polypaint_toggle(Operator):
    """Toggle vertex color painting in sculpt mode"""
    bl_idname = "spinner_sculptz.polypaint_toggle"
    bl_label = "Polypaint"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active mesh required")
            return {"CANCELLED"}
        mesh = obj.data
        # Ensure a color attribute exists
        if "Color" not in mesh.color_attributes:
            mesh.color_attributes.new(name="Color", type="BYTE_COLOR", domain="CORNER")
        # Switch to vertex paint if available, else stay in sculpt with color brush
        if context.mode == "SCULPT":
            # Prefer sculpt color brush if present
            brush = context.tool_settings.sculpt.brush
            if brush and hasattr(brush, "color"):
                self.report({"INFO"}, "Polypaint: use color brush in sculpt")
            else:
                bpy.ops.object.mode_set(mode="VERTEX_PAINT")
                self.report({"INFO"}, "Switched to Vertex Paint")
        else:
            bpy.ops.object.mode_set(mode="SCULPT")
            self.report({"INFO"}, "Back to Sculpt")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_add_layer(Operator):
    """Add a non-destructive sculpt layer (shape key)"""
    bl_idname = "spinner_sculptz.add_layer"
    bl_label = "Add Sculpt Layer"
    bl_options = {"REGISTER", "UNDO"}

    layer_name: StringProperty(name="Name", default="Layer")

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            return {"CANCELLED"}
        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis")
        sk = obj.shape_key_add(name=self.layer_name)
        sk.value = 1.0
        self.report({"INFO"}, f"Added layer: {sk.name}")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_project_detail(Operator):
    """Project detail from high-poly to active (Data Transfer)"""
    bl_idname = "spinner_sculptz.project_detail"
    bl_label = "Project Detail"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            return {"CANCELLED"}
        # Look for a selected high-poly source
        source = None
        for o in context.selected_objects:
            if o != obj and o.type == "MESH":
                source = o
                break
        if source is None:
            self.report({"WARNING"}, "Select a high-poly source mesh")
            return {"CANCELLED"}
        # Add Data Transfer modifier
        mod = obj.modifiers.new(name="ProjectDetail", type="DATA_TRANSFER")
        mod.object = source
        mod.use_vert_data = True
        mod.data_types_verts = {"VGROUP_WEIGHTS"}
        # Also try to transfer normals if available
        if hasattr(mod, "use_loop_data"):
            mod.use_loop_data = True
        self.report({"INFO"}, f"Projecting from {source.name}")
        return {"FINISHED"}


class SPINNER_SCULPTZ_OT_retopo(Operator):
    """ZRemesher-style retopo (calls Instant Meshes if available, else voxel remesh)"""
    bl_idname = "spinner_sculptz.retopo"
    bl_label = "Retopo"
    bl_options = {"REGISTER", "UNDO"}

    target_faces: bpy.props.IntProperty(name="Target Faces", default=8000, min=100, max=500000)

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            return {"CANCELLED"}
        # Prefer Instant Meshes wrapper if the operator exists
        if hasattr(bpy.ops, "spinner3d") and hasattr(bpy.ops.spinner3d, "instant_meshes"):
            bpy.ops.spinner3d.instant_meshes(target_faces=self.target_faces)
            self.report({"INFO"}, "Retopo via Instant Meshes")
            return {"FINISHED"}
        # Fallback: voxel remesh
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.voxel_remesh(voxel_size=0.02)
        bpy.ops.object.mode_set(mode="SCULPT")
        self.report({"INFO"}, "Retopo via voxel remesh")
        return {"FINISHED"}


classes = (
    SPINNER_SCULPTZ_OT_polypaint_toggle,
    SPINNER_SCULPTZ_OT_add_layer,
    SPINNER_SCULPTZ_OT_project_detail,
    SPINNER_SCULPTZ_OT_retopo,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
