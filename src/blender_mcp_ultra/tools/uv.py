"""UV mapping tools — unwrap, project, pack UVs."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def uv_smart_project(
    object_name: str,
    angle_limit: float = 66.0,
    island_margin: float = 0.02,
) -> dict:
    """Smart UV project unwrap.

    Args:
        object_name: Target mesh object.
        angle_limit: Angle limit in degrees.
        island_margin: Margin between islands.
    """
    conn = get_blender_connection()
    return conn.send_command("uv_smart_project", {
        "object_name": Validator.validate_name(object_name),
        "angle_limit": Validator.validate_float(angle_limit, 1, 180),
        "island_margin": Validator.validate_percentage(island_margin) / 100.0,
    })


@mcp.tool()
def uv_unwrap(object_name: str, method: str = "ANGLE_BASED") -> dict:
    """UV unwrap selected faces.

    Args:
        object_name: Target object.
        method: ANGLE_BASED or CONFORMAL.
    """
    conn = get_blender_connection()
    return conn.send_command("uv_unwrap", {
        "object_name": Validator.validate_name(object_name),
        "method": method.upper(),
    })


@mcp.tool()
def uv_pack_islands(
    object_name: str,
    margin: float = 0.001,
    rotate: bool = True,
) -> dict:
    """Pack UV islands to fill the UV space efficiently.

    Args:
        object_name: Target object.
        margin: Margin between islands.
        rotate: Allow islands to rotate.
    """
    conn = get_blender_connection()
    return conn.send_command("uv_pack_islands", {
        "object_name": Validator.validate_name(object_name),
        "margin": Validator.validate_percentage(margin) / 100.0,
        "rotate": rotate,
    })


@mcp.tool()
def uv_project_from_view(
    object_name: str,
    aspect_ratio: list[float] | None = None,
    direction: str = "VIEW",
) -> dict:
    """Project UVs from the current view or a specific direction.

    Args:
        object_name: Target object.
        aspect_ratio: [width, height] aspect ratio.
        direction: VIEW, TOP, FRONT, or SIDE.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "direction": direction.upper(),
    }
    if aspect_ratio:
        params["aspect_ratio"] = Validator.validate_vector(aspect_ratio, 2)
    return conn.send_command("uv_project_from_view", params)


@mcp.tool()
def uv_select_island(object_name: str, island_index: int = 0) -> dict:
    """Select a UV island by index.

    Args:
        object_name: Target object.
        island_index: Island index to select.
    """
    conn = get_blender_connection()
    return conn.send_command("uv_select_island", {
        "object_name": Validator.validate_name(object_name),
        "island_index": Validator.validate_int(island_index, 0, 1000),
    })


@mcp.tool()
def get_uv_info(object_name: str) -> dict:
    """Get UV mapping information: island count, UV bounds, stretch stats.

    Args:
        object_name: Target object.
    """
    conn = get_blender_connection()
    return conn.send_command("get_uv_info", {"object_name": Validator.validate_name(object_name)})
