"""File import/export handlers."""

import bpy
import os


def import_file(params: dict) -> dict:
    filepath = params["filepath"]
    file_type = params.get("file_type", "")

    if not file_type:
        ext = os.path.splitext(filepath)[1].lower()
        ext_map = {
            ".fbx": "FBX", ".obj": "OBJ", ".gltf": "GLTF", ".glb": "GLB",
            ".stl": "STL", ".usd": "USD", ".usda": "USD", ".usdc": "USD",
            ".abc": "ABC", ".ply": "PLY", ".dae": "COLLADA", ".3ds": "3DS",
        }
        file_type = ext_map.get(ext, "FBX")

    import_ops = {
        "FBX": lambda: bpy.ops.import_scene.fbx(filepath=filepath),
        "OBJ": lambda: bpy.ops.wm.obj_import(filepath=filepath),
        "GLTF": lambda: bpy.ops.import_scene.gltf(filepath=filepath),
        "GLB": lambda: bpy.ops.import_scene.gltf(filepath=filepath),
        "STL": lambda: bpy.ops.import_mesh.stl(filepath=filepath),
        "PLY": lambda: bpy.ops.import_mesh.ply(filepath=filepath),
        "USD": lambda: bpy.ops.wm.usd_import(filepath=filepath),
        "ABC": lambda: bpy.ops.wm.alembic_import(filepath=filepath),
    }

    op = import_ops.get(file_type)
    if op:
        op()
        return {"status": "imported", "filepath": filepath, "type": file_type}
    return {"error": f"Unsupported file type: {file_type}"}


def export_file(params: dict) -> dict:
    filepath = params["filepath"]
    file_type = params.get("file_type", "")

    if not file_type:
        ext = os.path.splitext(filepath)[1].lower()
        ext_map = {
            ".fbx": "FBX", ".obj": "OBJ", ".gltf": "GLTF", ".glb": "GLB",
            ".stl": "STL", ".usd": "USD", ".abc": "ABC", ".ply": "PLY",
        }
        file_type = ext_map.get(ext, "FBX")

    selected = params.get("selected_only", False)

    export_ops = {
        "FBX": lambda: bpy.ops.export_scene.fbx(filepath=filepath, use_selection=selected),
        "OBJ": lambda: bpy.ops.wm.obj_export(filepath=filepath, export_selected_objects=selected),
        "GLTF": lambda: bpy.ops.export_scene.gltf(filepath=filepath, use_selection=selected),
        "GLB": lambda: bpy.ops.export_scene.gltf(filepath=filepath, use_selection=selected, export_format='GLB'),
        "STL": lambda: bpy.ops.export_mesh.stl(filepath=filepath, use_selection=selected),
        "PLY": lambda: bpy.ops.export_mesh.ply(filepath=filepath, use_selection=selected),
        "USD": lambda: bpy.ops.wm.usd_export(filepath=filepath, export_selected_objects=selected),
        "ABC": lambda: bpy.ops.wm.alembic_export(filepath=filepath, selection=selected),
    }

    op = export_ops.get(file_type)
    if op:
        op()
        return {"status": "exported", "filepath": filepath, "type": file_type}
    return {"error": f"Unsupported file type: {file_type}"}


def export_fbx(params: dict) -> dict:
    return export_file({**params, "file_type": "FBX"})


def export_glb(params: dict) -> dict:
    return export_file({**params, "file_type": "GLB"})


def export_obj(params: dict) -> dict:
    return export_file({**params, "file_type": "OBJ"})


HANDLERS = {
    "import_file": import_file,
    "export_file": export_file,
    "export_fbx": export_fbx,
    "export_glb": export_glb,
    "export_obj": export_obj,
}
