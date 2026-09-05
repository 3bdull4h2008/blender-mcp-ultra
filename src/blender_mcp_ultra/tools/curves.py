"""Curve tools — create and manipulate curves, text objects."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_curve(
    name: str = "Curve",
    curve_type: str = "BEZIER",
    points: list[list[float]] = None,
    location: list[float] = None,
    bevel_depth: float = 0.0,
    bevel_resolution: int = 0,
    fill: str = "FULL",
) -> dict:
    """Create a curve object.

    Args:
        name: Curve name.
        curve_type: BEZIER, NURBS, or POLY.
        points: List of [x, y, z] control points.
        location: [x, y, z] position.
        bevel_depth: Curve bevel depth (thickness).
        bevel_resolution: Bevel resolution.
        fill: FULL, HALF, or NONE.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "curve_type": curve_type.upper(),
        "bevel_depth": Validator.validate_float(bevel_depth, 0, 100),
        "bevel_resolution": Validator.validate_int(bevel_resolution, 0, 32),
        "fill": fill.upper(),
    }
    if points:
        params["points"] = [Validator.validate_vector(p) for p in points]
    if location:
        params["location"] = Validator.validate_vector(location)
    return conn.send_command("create_curve", params)


@mcp.tool()
def create_text_object(
    name: str = "Text",
    text: str = "Hello",
    location: list[float] = None,
    size: float = 1.0,
    extrude: float = 0.0,
    font_path: str = "",
) -> dict:
    """Create a text object with formatting.

    Args:
        name: Object name.
        text: The text content.
        location: [x, y, z] position.
        size: Font size.
        extrude: Text depth.
        font_path: Path to a .ttf/.otf font file.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "text": text,
        "size": Validator.validate_float(size, 0.01, 1000),
        "extrude": Validator.validate_float(extrude, 0, 100),
    }
    if location:
        params["location"] = Validator.validate_vector(location)
    if font_path:
        params["font_path"] = Validator.validate_path(font_path)
    return conn.send_command("create_text_object", params)


@mcp.tool()
def edit_curve_points(
    curve_name: str,
    action: str = "add",
    points: list[list[float]] = None,
    index: int = -1,
) -> dict:
    """Add or remove curve control points.

    Args:
        curve_name: Curve object name.
        action: add, remove, or move.
        points: [x, y, z] for add/move actions.
        index: Point index for remove/move (-1 = last).
    """
    conn = get_blender_connection()
    params = {
        "curve_name": Validator.validate_name(curve_name),
        "action": action.lower(),
        "index": Validator.validate_int(index, -1, 10000),
    }
    if points:
        params["points"] = [Validator.validate_vector(p) for p in points]
    return conn.send_command("edit_curve_points", params)


@mcp.tool()
def set_curve_fill(curve_name: str, fill: str = "FULL") -> dict:
    """Set curve fill mode.

    Args:
        curve_name: Curve object name.
        fill: FULL, HALF, or NONE.
    """
    conn = get_blender_connection()
    return conn.send_command("set_curve_fill", {
        "curve_name": Validator.validate_name(curve_name),
        "fill": fill.upper(),
    })


@mcp.tool()
def convert_curve_to_mesh(curve_name: str, name: str = "") -> dict:
    """Convert a curve object to a mesh.

    Args:
        curve_name: Curve to convert.
        name: Name for the new mesh. Empty = auto.
    """
    conn = get_blender_connection()
    params = {"curve_name": Validator.validate_name(curve_name)}
    if name:
        params["name"] = Validator.validate_name(name)
    return conn.send_command("convert_curve_to_mesh", params)
