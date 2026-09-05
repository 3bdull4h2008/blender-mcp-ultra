"""Code execution handlers — run Python in Blender."""

import bpy
import os

SAFE_MODULES = {"bpy", "bmesh", "mathutils", "math", "json", "random"}

ALLOWED_OPERATORS = {
    "bpy.ops.mesh.select_all",
    "bpy.ops.mesh.select_more",
    "bpy.ops.mesh.select_less",
    "bpy.ops.mesh.select_non_manifold",
    "bpy.ops.mesh.select_loose",
    "bpy.ops.mesh.normals_make_consistent",
    "bpy.ops.mesh.remove_doubles",
    "bpy.ops.mesh.extrude_region_move",
    "bpy.ops.mesh.bevel",
    "bpy.ops.mesh.subdivide",
    "bpy.ops.mesh.triangulate",
    "bpy.ops.mesh.quads_convert_to_tris",
    "bpy.ops.mesh.tris_to_quads",
    "bpy.ops.mesh.dissolve_limited",
    "bpy.ops.mesh.fill",
    "bpy.ops.mesh.grid_fill",
    "bpy.ops.mesh.poke_faces",
    "bpy.ops.mesh.mark_seam",
    "bpy.ops.mesh.clear_seam",
    "bpy.ops.mesh.mark_sharp",
    "bpy.ops.mesh.smooth_vertices",
    "bpy.ops.object.mode_set",
    "bpy.ops.object.select_all",
    "bpy.ops.object.delete",
    "bpy.ops.object.duplicate_move",
    "bpy.ops.object.join",
    "bpy.ops.object.origin_set",
    "bpy.ops.object.shade_smooth",
    "bpy.ops.object.shade_flat",
    "bpy.ops.object.transform_apply",
    "bpy.ops.object.parent_clear",
    "bpy.ops.transform.translate",
    "bpy.ops.transform.rotate",
    "bpy.ops.transform.resize",
    "bpy.ops.view3d.snap_cursor_to_center",
    "bpy.ops.view3d.snap_selected_to_cursor",
    "bpy.ops.view3d.snap_cursor_to_selected",
    "bpy.ops.render.render",
    "bpy.ops.wm.save_mainfile",
    "bpy.ops.wm.open_mainfile",
    "bpy.ops.uv.smart_project",
    "bpy.ops.uv.unwrap",
    "bpy.ops.uv.pack_islands",
    "bpy.ops.material.new",
    "bpy.ops.object.armature_add",
    "bpy.ops.curve.bezier_circle_add",
    "bpy.ops.mesh.primitive_cube_add",
    "bpy.ops.mesh.primitive_uv_sphere_add",
    "bpy.ops.mesh.primitive_cylinder_add",
    "bpy.ops.mesh.primitive_cone_add",
    "bpy.ops.mesh.primitive_torus_add",
    "bpy.ops.mesh.primitive_plane_add",
    "bpy.ops.mesh.primitive_ico_sphere_add",
    "bpy.ops.mesh.primitive_monkey_add",
}


def execute_blender_code(params: dict) -> dict:
    code = params.get("code", "")
    if not code:
        return {"error": "No code provided"}

    try:
        result = {}
        safe_builtins = {k: __builtins__[k] if isinstance(__builtins__, dict) else getattr(__builtins__, k)
                         for k in ("abs", "min", "max", "len", "range", "int", "float", "str", "list",
                                   "dict", "tuple", "set", "bool", "enumerate", "zip", "map", "filter",
                                   "sorted", "reversed", "sum", "round", "any", "all", "isinstance",
                                   "type", "print", "True", "False", "None", "Exception", "ValueError",
                                   "TypeError", "KeyError", "IndexError", "AttributeError")
                         if (isinstance(__builtins__, dict) and k in __builtins__) or
                            (not isinstance(__builtins__, dict) and hasattr(__builtins__, k))}
        exec(compile(code, "<blender_mcp>", "exec"), {"bpy": bpy, "__result__": result, "__builtins__": safe_builtins})
        return {"status": "executed", "code_length": len(code)}
    except Exception as e:
        return {"error": f"Execution failed: {type(e).__name__}: {e}"}


def execute_blender_script(params: dict) -> dict:
    script_path = params.get("script_path", "")
    if not script_path:
        return {"error": "No script path provided"}

    if not os.path.exists(script_path):
        return {"error": f"Script not found: {script_path}"}

    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, script_path, "exec"), {"bpy": bpy})
        return {"status": "script_executed", "path": script_path}
    except Exception as e:
        return {"error": f"Script failed: {type(e).__name__}: {e}"}


def run_operator(params: dict) -> dict:
    operator_name = params.get("operator_name", "")
    if not operator_name:
        return {"error": "No operator name provided"}

    parts = operator_name.split(".")
    if len(parts) < 3:
        return {"error": f"Invalid operator format: {operator_name}. Use 'bpy.ops.category.operator_name'"}

    op_str = ".".join(parts[:3])
    if op_str not in ALLOWED_OPERATORS:
        return {"error": f"Operator '{operator_name}' is not in the allowed list. Use execute_blender_code for custom operators."}

    try:
        import bpy.ops
        op_module = getattr(bpy.ops, parts[1])
        op_func = getattr(op_module, parts[2])
        kwargs = {k: v for k, v in params.items() if k != "operator_name"}
        result = op_func(**kwargs) if kwargs else op_func()
        return {"status": "operator_executed", "operator": operator_name}
    except AttributeError:
        return {"error": f"Operator '{operator_name}' not found"}
    except Exception as e:
        return {"error": f"Operator failed: {type(e).__name__}: {e}"}


HANDLERS = {
    "execute_blender_code": execute_blender_code,
    "execute_blender_script": execute_blender_script,
    "run_operator": run_operator,
}
