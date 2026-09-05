"""Code execution tools — run arbitrary Python in Blender with safety controls."""

import logging

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator

logger = logging.getLogger("blender_mcp_ultra.code_exec")


@mcp.tool()
def execute_blender_code(code: str) -> dict:
    """Execute arbitrary Python code in Blender with full bpy access.

    WARNING: This runs unvalidated code. Use structured tools when possible.
    Code is executed in a sandboxed environment with restricted builtins.

    Args:
        code: Python code to execute. Has access to 'bpy' and 'bmesh'.
    """
    conn = get_blender_connection()
    code = Validator.validate_blender_code(code)
    warnings = Validator.check_code_safety(code)
    if warnings:
        logger.warning("Code safety warnings: %s", warnings)
    return conn.send_command("execute_blender_code", {"code": code})


@mcp.tool()
def execute_blender_script(script_path: str) -> dict:
    """Execute a Python script file in Blender.

    Args:
        script_path: Path to the .py script file.
    """
    conn = get_blender_connection()
    return conn.send_command("execute_blender_script", {
        "script_path": Validator.validate_path(script_path),
    })


@mcp.tool()
def run_operator(operator_name: str, **kwargs) -> dict:
    """Execute a bpy.ops operator by name.

    Args:
        operator_name: Full operator name (e.g., 'mesh.primitive_cube_add').
        **kwargs: Operator parameters.
    """
    conn = get_blender_connection()
    params = {"operator_name": operator_name}
    params.update(kwargs)
    return conn.send_command("run_operator", params)
