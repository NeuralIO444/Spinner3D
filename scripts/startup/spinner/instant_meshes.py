# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Instant Meshes subprocess wrapper
# Binary path is set in Preferences. No binary is bundled.

import os
import subprocess
import tempfile

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty



class SPINNER3D_AddonPreferences(AddonPreferences):
    bl_idname = __package__ or "spinner"

    instant_meshes_binary: StringProperty(
        name="Instant Meshes Binary",
        description="Full path to the Instant Meshes executable",
        subtype="FILE_PATH",
        default="",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "instant_meshes_binary")


class SPINNER3D_OT_instant_meshes(Operator):
    """Remesh active object with Instant Meshes (subprocess)"""
    bl_idname = "spinner3d.instant_meshes"
    bl_label = "Remesh: Instant Meshes"
    bl_options = {"REGISTER", "UNDO"}

    target_faces: IntProperty(
        name="Target Faces",
        default=10000,
        min=100,
        max=1000000,
    )

    def execute(self, context):
        prefs = context.preferences.addons.get(__package__)
        if prefs is None:
            # Fallback: look for the preference on the package name used by Blender
            prefs = context.preferences.addons.get("spinner")
        binary = ""
        if prefs and hasattr(prefs.preferences, "instant_meshes_binary"):
            binary = prefs.preferences.instant_meshes_binary
        if not binary or not os.path.isfile(binary):
            self.report(
                {"ERROR"},
                "Instant Meshes binary not set or not found. Set it in Preferences > Add-ons > Spinner3D.",
            )
            return {"CANCELLED"}

        obj = context.active_object
        if not obj or obj.type != "MESH":
            self.report({"WARNING"}, "Active mesh required")
            return {"CANCELLED"}

        with tempfile.TemporaryDirectory() as tmp:
            in_path = os.path.join(tmp, "input.obj")
            out_path = os.path.join(tmp, "output.obj")

            # Export active object
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.wm.obj_export(
                filepath=in_path,
                export_selected_objects=True,
                export_materials=False,
            )

            # Run Instant Meshes (CLI)
            cmd = [
                binary,
                in_path,
                "-o",
                out_path,
                "-f",
                str(self.target_faces),
                "-d",  # deterministic
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            except subprocess.CalledProcessError as e:
                self.report({"ERROR"}, f"Instant Meshes failed: {e.stderr.decode()[:200]}")
                return {"CANCELLED"}
            except subprocess.TimeoutExpired:
                self.report({"ERROR"}, "Instant Meshes timed out")
                return {"CANCELLED"}
            except FileNotFoundError:
                self.report({"ERROR"}, "Instant Meshes binary not executable")
                return {"CANCELLED"}

            if not os.path.isfile(out_path):
                self.report({"ERROR"}, "Instant Meshes produced no output")
                return {"CANCELLED"}

            # Import result
            bpy.ops.wm.obj_import(filepath=out_path)
            imported = context.selected_objects[-1] if context.selected_objects else None
            if imported:
                imported.name = f"{obj.name}_IM"
                imported.location = obj.location

        self.report({"INFO"}, "Instant Meshes remesh complete")
        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(SPINNER3D_OT_instant_meshes.bl_idname, icon="MESH_GRID")


classes = (SPINNER3D_AddonPreferences, SPINNER3D_OT_instant_meshes,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
