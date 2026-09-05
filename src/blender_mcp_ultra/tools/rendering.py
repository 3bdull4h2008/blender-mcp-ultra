"""Rendering tools — trigger renders, capture viewport, get results."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def render_image(
    output_path: str = "",
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    samples: int = 128,
    engine: str = "CYCLES",
) -> dict:
    """Render the current scene to an image file.

    Args:
        output_path: File path for the rendered image. If empty, uses temp file.
        resolution_x: Output width.
        resolution_y: Output height.
        samples: Render samples.
        engine: BLENDER_EEVEE, CYCLES, or BLENDER_WORKBENCH.
    """
    conn = get_blender_connection()
    params = {
        "resolution_x": Validator.validate_int(resolution_x, 64, 16384),
        "resolution_y": Validator.validate_int(resolution_y, 64, 16384),
        "samples": Validator.validate_int(samples, 1, 10000),
        "engine": Validator.validate_enum(engine, "render_engine"),
    }
    if output_path:
        params["output_path"] = Validator.validate_path(output_path)
    return conn.send_command("render_image", params)


@mcp.tool()
def render_animation(
    output_path: str = "",
    frame_start: int = 1,
    frame_end: int = 250,
    engine: str = "CYCLES",
) -> dict:
    """Render an animation sequence.

    Args:
        output_path: Output directory path.
        frame_start: First frame.
        frame_end: Last frame.
        engine: Render engine.
    """
    conn = get_blender_connection()
    params = {
        "frame_start": Validator.validate_int(frame_start, 0, 1000000),
        "frame_end": Validator.validate_int(frame_end, 1, 1000000),
        "engine": Validator.validate_enum(engine, "render_engine"),
    }
    if output_path:
        params["output_path"] = Validator.validate_path(output_path)
    return conn.send_command("render_animation", params)


@mcp.tool()
def render_preview(
    quality: str = "MEDIUM",
) -> dict:
    """Quick preview render for visual feedback loops.

    Args:
        quality: LOW (320x240), MEDIUM (800x600), HIGH (1920x1080).
    """
    conn = get_blender_connection()
    return conn.send_command("render_preview", {"quality": quality.upper()})
