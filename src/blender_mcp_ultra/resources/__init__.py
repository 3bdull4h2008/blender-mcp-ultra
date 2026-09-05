"""MCP Resources — scene state, objects, materials as queryable resources."""

import json

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp


@mcp.resource("blender://scene")
def get_scene_resource() -> str:
    """Full scene information: objects, hierarchy, frame range, render engine, FPS."""
    conn = get_blender_connection()
    result = conn.send_command("get_scene_info")
    return json.dumps(result, indent=2)


@mcp.resource("blender://objects")
def get_objects_resource() -> str:
    """List of all objects with name, type, location, and visibility."""
    conn = get_blender_connection()
    result = conn.send_command("list_objects", {"object_type": "ALL", "include_hidden": False})
    return json.dumps(result, indent=2)


@mcp.resource("blender://materials")
def get_materials_resource() -> str:
    """List of all materials with name and user count."""
    conn = get_blender_connection()
    result = conn.send_command("list_materials")
    return json.dumps(result, indent=2)
