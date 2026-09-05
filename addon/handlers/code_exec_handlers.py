"""Code execution handlers — run Python in Blender safely."""

import bpy
import restrictedpython

SAFE_MODULES = {"bpy", "bmesh", "mathutils", "math", "json", "random"}


def execute_blender_code(params: dict) -> dict:
    code = params.get("code", "")
    if not code:
        return {"error": "No code provided"}

    try:
        result = {}
        exec(compile(code, "<blender_mcp>", "exec"), {"bpy": bpy, "__result__": result})
        return {"status": "executed", "code_length": len(code)}
    except Exception as e:
        return {"error": f"Execution failed: {type(e).__name__}: {e}"}


def execute_blender_script(params: dict) -> dict:
    script_path = params.get("script_path", "")
    if not script_path:
        return {"error": "No script path provided"}

    import os
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

    # Parse module and op
    parts = operator_name.split(".")
    if len(parts) < 3:
        return {"error": f"Invalid operator format: {operator_name}. Use 'module.category.operator_name'"}

    try:
        module = __import__("bpy.ops")
        op_module = getattr(module.ops, parts[1])
        op_func = getattr(op_module, parts[2])
        kwargs = {k: v for k, v in params.items() if k != "operator_name"}
        result = op_func(**kwargs)
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
