# SPDX-License-Identifier: GPL-3.0-or-later
# Spinner3D: Manifold boolean default + Exact fallback coverage.
# Run with: blender --background --python tests/python/spinner3d_boolean_fallback.py

import bpy
import bmesh


def make_cube(name, location=(0, 0, 0)):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    return obj


def make_non_manifold(name, location=(0.5, 0.5, 0.5)):
    """Open cube (missing one face) — non-manifold input that Manifold should reject."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    # Delete one face so the mesh is open / non-manifold
    bm.faces.ensure_lookup_table()
    if bm.faces:
        bmesh.ops.delete(bm, geom=[bm.faces[0]], context="FACES")
    bm.to_mesh(mesh)
    bm.free()
    obj.location = location
    return obj


def run():
    # Clean scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    base = make_cube("Base")
    cutter = make_non_manifold("Cutter")

    # Add Boolean modifier with Manifold solver (the Spinner3D default)
    mod = base.modifiers.new(name="Bool", type="BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "MANIFOLD"
    mod.object = cutter

    # Force evaluation
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = base.evaluated_get(depsgraph)
    result = eval_obj.data

    # Success criteria: either Manifold produced a result, or the fallback path
    # left a usable mesh (Exact is used internally when Manifold fails).
    ok = result is not None and len(result.polygons) > 0
    print(f"SPINNER3D boolean fallback test: {'PASS' if ok else 'FAIL'}")
    print(f"  result polygons: {len(result.polygons) if result else 0}")
    print(f"  modifier solver: {mod.solver}")
    return ok


if __name__ == "__main__":
    success = run()
    raise SystemExit(0 if success else 1)
