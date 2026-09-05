"""MCP Server — bridges AI agents to Blender via structured tools."""

import asyncio
import logging
import sys

from mcp.server.fastmcp import FastMCP

from blender_mcp_ultra.connection import BlenderConnection, get_blender_connection
from blender_mcp_ultra.validators import Validator

logger = logging.getLogger("blender_mcp_ultra")

mcp = FastMCP(
    "blender-mcp-ultra",
    instructions="""You are an expert 3D artist controlling Blender through structured MCP tools.
Follow these principles:
1. ALWAYS start by calling get_scene_info to understand the current scene
2. Use structured tools instead of execute_blender_code whenever possible
3. After significant changes, call get_viewport_screenshot to verify your work
4. Use analyze_mesh_quality to check for geometry defects before finalizing
5. Follow the expert prompts for topology, lighting, materials, and scale
6. Group related operations and use auto-undo for reversible workflows
7. When in doubt, use get_object_info to inspect before modifying""",
)


def _register_all_tools():
    """Import all tool modules to register them with the MCP server."""
    from blender_mcp_ultra.tools import (
        animation,
        armature,
        camera,
        code_exec,
        collections,
        curves,
        file_ops,
        geometry_nodes,
        lighting,
        materials,
        mesh_editing,
        mesh_quality,
        modeling,
        objects,
        physics,
        procedural,
        rendering,
        scene,
        screenshot,
        sculpting,
        transforms,
        uv,
        viewport,
    )


def _register_all_prompts():
    """Import all prompt modules to register them with the MCP server."""
    from blender_mcp_ultra.prompts import workflows


def _register_all_resources():
    """Import all resource modules to register them with the MCP server."""
    from blender_mcp_ultra.resources import scene_info


def main():
    """Run the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    _register_all_tools()
    _register_all_prompts()
    _register_all_resources()

    logger.info("blender-mcp-ultra v%s starting", __import__("blender_mcp_ultra").__version__)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
