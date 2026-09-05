"""Blender MCP Ultra Addon — runs inside Blender to handle AI agent commands."""

bl_info = {
    "name": "Blender MCP Ultra",
    "author": "Blender MCP Ultra",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > MCP Ultra",
    "description": "MCP server addon for AI agent control of Blender",
    "category": "System",
}

import bpy

from .server import BlenderMCPServer

_server_instance = None


def register():
    global _server_instance
    _server_instance = BlenderMCPServer()
    _server_instance.register()
    print("[Blender MCP Ultra] Addon registered. Start server from View3D > Sidebar > MCP Ultra tab.")


def unregister():
    global _server_instance
    if _server_instance:
        _server_instance.unregister()
        _server_instance = None
    print("[Blender MCP Ultra] Addon unregistered.")
