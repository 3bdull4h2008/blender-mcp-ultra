"""Viewport and screenshot tools — visual feedback for AI agents."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp


@mcp.tool()
def get_viewport_screenshot(
    mode: str = "fast",
    resolution: str = "MEDIUM",
) -> dict:
    """Capture a screenshot of the 3D viewport for visual feedback.

    Args:
        mode: FAST (OpenGL, ms) or QUALITY (full render, seconds).
        resolution: LOW, MEDIUM, HIGH, or ULTRA.
    Returns:
        Base64-encoded PNG image data.
    """
    conn = get_blender_connection()
    return conn.send_command("get_viewport_screenshot", {
        "mode": mode.lower(),
        "resolution": resolution.upper(),
    })


@mcp.tool()
def get_render_preview() -> dict:
    """Get a quick render preview of the current scene.

    Returns base64-encoded PNG of a fast preview render.
    """
    conn = get_blender_connection()
    return conn.send_command("get_render_preview")


@mcp.tool()
def get_viewport_info() -> dict:
    """Get current viewport state: active camera, shading mode, view matrix, cursor position."""
    conn = get_blender_connection()
    return conn.send_command("get_viewport_info")


@mcp.tool()
def set_viewport_shading(mode: str = "SOLID") -> dict:
    """Set viewport shading mode.

    Args:
        mode: WIREFRAME, SOLID, MATERIAL, or RENDERED.
    """
    conn = get_blender_connection()
    return conn.send_command("set_viewport_shading", {"mode": mode.upper()})


@mcp.tool()
def set_viewport_camera(camera_name: str = "") -> dict:
    """Set the active viewport camera.

    Args:
        camera_name: Camera to use. Empty string = auto.
    """
    conn = get_blender_connection()
    return conn.send_command("set_viewport_camera", {"camera_name": camera_name})


@mcp.tool()
def toggle_overlays(show: bool = True) -> dict:
    """Toggle viewport overlays (grid, axes, selection outlines).

    Args:
        show: True to show overlays, False to hide.
    """
    conn = get_blender_connection()
    return conn.send_command("toggle_overlays", {"show": show})
