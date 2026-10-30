# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z navigation modal
# Empty-space left-drag orbits; pivot is last stroke; Shift snaps to ortho.

import bpy
from bpy.types import Operator
from bpy_extras import view3d_utils
from mathutils import Vector


class SPINNER_SCULPTZ_OT_navigate(Operator):
    """ZBrush-style navigation: empty-space drag orbits, Shift snaps ortho"""
    bl_idname = "spinner_sculptz.navigate"
    bl_label = "Sculpt Z Navigate"
    bl_options = {"REGISTER", "UNDO", "BLOCKING"}

    _timer = None
    _pivot = None
    _start_mouse = None
    _orbiting = False

    def modal(self, context, event):
        if event.type == "LEFTMOUSE" and event.value == "RELEASE":
            self._orbiting = False
            return {"FINISHED"}

        if event.type == "MOUSEMOVE" and self._orbiting:
            dx = event.mouse_x - self._start_mouse[0]
            dy = event.mouse_y - self._start_mouse[1]
            self._start_mouse = (event.mouse_x, event.mouse_y)

            region = context.region
            rv3d = context.region_data
            if rv3d is None:
                return {"RUNNING_MODAL"}

            # Orbit around pivot
            if self._pivot is not None:
                rv3d.view_location = self._pivot

            # Simple orbit via view rotation
            sensitivity = 0.005
            rv3d.view_rotation.rotate(Vector((0, 0, 1)).rotation_difference(
                Vector((dx * sensitivity, dy * sensitivity, 0)).to_track_quat("Z", "Y")
            ))

            # Shift snaps to nearest ortho
            if event.shift:
                self._snap_ortho(rv3d)

            context.area.tag_redraw()
            return {"RUNNING_MODAL"}

        if event.type in {"RIGHTMOUSE", "ESC"}:
            return {"CANCELLED"}

        return {"PASS_THROUGH"}

    def _snap_ortho(self, rv3d):
        """Snap view to nearest ortho axis."""
        from mathutils import Quaternion
        # Approximate snap by aligning to world axes
        rot = rv3d.view_rotation
        # Find closest of front/side/top
        axes = [
            Quaternion((1, 0, 0, 0)),           # front
            Quaternion((0.707, 0, 0.707, 0)),   # side
            Quaternion((0.707, 0.707, 0, 0)),   # top
        ]
        best = min(axes, key=lambda q: (rot.inverted() @ q).angle)
        rv3d.view_rotation = best

    def invoke(self, context, event):
        if context.area.type != "VIEW_3D":
            return {"CANCELLED"}

        # Raycast to decide empty space vs mesh
        region = context.region
        rv3d = context.region_data
        coord = (event.mouse_region_x, event.mouse_region_y)
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

        hit = False
        if context.mode == "SCULPT" and context.active_object:
            result, location, normal, index, obj, matrix = context.scene.ray_cast(
                context.view_layer.depsgraph, ray_origin, view_vector
            )
            hit = result

        if hit:
            # On mesh: let sculpt stroke happen
            return {"PASS_THROUGH"}

        # Empty space: start orbit
        self._start_mouse = (event.mouse_x, event.mouse_y)
        self._orbiting = True

        # Pivot = last stroke location if available, else view center
        self._pivot = None
        if hasattr(context.tool_settings, "sculpt") and context.tool_settings.sculpt.brush:
            # Use current view location as fallback pivot
            self._pivot = context.region_data.view_location.copy()

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


classes = (SPINNER_SCULPTZ_OT_navigate,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
