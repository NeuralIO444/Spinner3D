# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D Sculpt Z shelf / side strip

import bpy
from bpy.types import Panel


class SPINNER_SCULPTZ_PT_shelf(Panel):
    """Dense top shelf / side strip for Sculpt Z"""
    bl_label = "Sculpt Z"
    bl_idname = "SPINNER_SCULPTZ_PT_shelf"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Sculpt Z"

    def draw(self, context):
        layout = self.layout
        layout.operator("spinner_sculptz.enter", icon="SCULPTMODE_HLT")
        layout.operator("spinner_sculptz.exit", icon="LOOP_BACK")

        layout.separator()
        layout.label(text="Brushes")
        row = layout.row(align=True)
        row.operator("spinner_sculptz.apply_brush", text="Move").brush_name = "Move"
        row.operator("spinner_sculptz.apply_brush", text="Clay").brush_name = "ClayBuildup"
        row = layout.row(align=True)
        row.operator("spinner_sculptz.apply_brush", text="Dam").brush_name = "DamStandard"
        row.operator("spinner_sculptz.apply_brush", text="Polish").brush_name = "hPolish"

        layout.separator()
        layout.label(text="Mesh")
        layout.operator("spinner_sculptz.dynamesh", icon="MOD_REMESH")
        row = layout.row(align=True)
        row.operator("spinner_sculptz.subdiv_up", text="Subdiv +")
        row.operator("spinner_sculptz.subdiv_down", text="Subdiv -")
        row = layout.row(align=True)
        row.operator("spinner_sculptz.isolate", text="Isolate")
        row.operator("spinner_sculptz.show_all", text="Show All")

        layout.separator()
        layout.label(text="Phase 2")
        layout.operator("spinner_sculptz.polypaint_toggle", icon="VPAINT_HLT")
        layout.operator("spinner_sculptz.add_layer", icon="SHAPEKEY_DATA")
        layout.operator("spinner_sculptz.project_detail", icon="MOD_DATA_TRANSFER")
        layout.operator("spinner_sculptz.retopo", icon="MOD_REMESH")


classes = (SPINNER_SCULPTZ_PT_shelf,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
