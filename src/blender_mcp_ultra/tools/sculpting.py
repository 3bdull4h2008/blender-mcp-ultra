"""Sculpting tools — brush configuration, sculpt mode operations."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def configure_sculpt_brush(
    brush_name: str = "Draw",
    size: float = 50.0,
    strength: float = 0.5,
    auto_masking: bool = False,
) -> dict:
    """Configure the active sculpt brush.

    Args:
        brush_name: Draw, Clay, Crease, Inflate, Grab, Smooth, etc.
        size: Brush radius.
        strength: Brush strength (0-1).
        auto_masking: Enable auto masking.
    """
    conn = get_blender_connection()
    return conn.send_command("configure_sculpt_brush", {
        "brush_name": brush_name,
        "size": Validator.validate_float(size, 1, 1000),
        "strength": Validator.validate_percentage(strength) / 100.0,
        "auto_masking": auto_masking,
    })


@mcp.tool()
def enter_sculpt_mode(object_name: str = "") -> dict:
    """Enter sculpt mode on an object.

    Args:
        object_name: Object to sculpt. Empty = active object.
    """
    conn = get_blender_connection()
    return conn.send_command("enter_sculpt_mode", {"object_name": object_name})


@mcp.tool()
def exit_sculpt_mode() -> dict:
    """Exit sculpt mode and return to object mode."""
    conn = get_blender_connection()
    return conn.send_command("exit_sculpt_mode")


@mcp.tool()
def set_sculpt_symmetry(
    axis_x: bool = True,
    axis_y: bool = False,
    axis_z: bool = False,
    mirror: bool = True,
) -> dict:
    """Configure sculpt symmetry settings.

    Args:
        axis_x: Mirror on X axis.
        axis_y: Mirror on Y axis.
        axis_z: Mirror on Z axis.
        mirror: Enable mirroring.
    """
    conn = get_blender_connection()
    return conn.send_command("set_sculpt_symmetry", {
        "axis_x": axis_x,
        "axis_y": axis_y,
        "axis_z": axis_z,
        "mirror": mirror,
    })


@mcp.tool()
def configure_dyntopo(
    enabled: bool = True,
    detail_size: float = 12.0,
    resolution: str = "RELATIVE",
) -> dict:
    """Configure dynamic topology (dyntopo) for sculpting.

    Args:
        enabled: Enable/disable dyntopo.
        detail_size: Detail size (smaller = more detail).
        resolution: RELATIVE, ABSOLUTE, or BRUSH.
    """
    conn = get_blender_connection()
    return conn.send_command("configure_dyntopo", {
        "enabled": enabled,
        "detail_size": Validator.validate_float(detail_size, 1, 100),
        "resolution": resolution.upper(),
    })


@mcp.tool()
def remesh_sculpt(
    mode: str = "VOXEL",
    voxel_size: float = 0.1,
    smooth_iterations: int = 2,
) -> dict:
    """Remesh the active object for sculpting.

    Args:
        mode: VOXEL or SMOOTH.
        voxel_size: Voxel size for voxel remesh.
        smooth_iterations: Smooth iterations for smooth remesh.
    """
    conn = get_blender_connection()
    return conn.send_command("remesh_sculpt", {
        "mode": mode.upper(),
        "voxel_size": Validator.validate_float(voxel_size, 0.001, 10),
        "smooth_iterations": Validator.validate_int(smooth_iterations, 0, 50),
    })
