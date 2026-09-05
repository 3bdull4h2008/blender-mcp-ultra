"""Viewport screenshot tool — separate for clean import."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp


@mcp.tool()
def take_screenshot(
    filepath: str = "",
    width: int = 800,
    height: int = 600,
) -> dict:
    """Take a viewport screenshot and optionally save to file.

    Args:
        filepath: Path to save the image. If empty, returns base64 only.
        width: Output width in pixels.
        height: Output height in pixels.
    """
    conn = get_blender_connection()
    params = {"width": width, "height": height}
    if filepath:
        params["filepath"] = filepath
    return conn.send_command("take_screenshot", params)
