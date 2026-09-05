"""Modeling tools — mesh operations, modifiers, boolean operations."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def add_modifier(
    object_name: str,
    modifier_type: str,
    name: str = "",
    **kwargs,
) -> dict:
    """Add a modifier to an object.

    Args:
        object_name: Target object.
        modifier_type: SUBSURF, MIRROR, SOLIDIFY, BOOLEAN, BEVEL, ARRAY, etc.
        name: Optional modifier name.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "modifier_type": modifier_type.upper(),
    }
    if name:
        params["name"] = Validator.validate_name(name)
    params.update(kwargs)
    return conn.send_command("add_modifier", params)


@mcp.tool()
def configure_modifier(
    object_name: str,
    modifier_name: str,
    settings: dict,
) -> dict:
    """Configure settings of an existing modifier.

    Args:
        object_name: Target object.
        modifier_name: Name of the modifier to configure.
        settings: Dict of setting_name: value pairs.
    """
    conn = get_blender_connection()
    return conn.send_command("configure_modifier", {
        "object_name": Validator.validate_name(object_name),
        "modifier_name": Validator.validate_name(modifier_name),
        "settings": settings,
    })


@mcp.tool()
def apply_modifier(object_name: str, modifier_name: str) -> dict:
    """Apply (bake) a modifier into the mesh.

    Args:
        object_name: Target object.
        modifier_name: Name of the modifier to apply.
    """
    conn = get_blender_connection()
    return conn.send_command("apply_modifier", {
        "object_name": Validator.validate_name(object_name),
        "modifier_name": Validator.validate_name(modifier_name),
    })


@mcp.tool()
def remove_modifier(object_name: str, modifier_name: str) -> dict:
    """Remove a modifier from an object.

    Args:
        object_name: Target object.
        modifier_name: Name of the modifier to remove.
    """
    conn = get_blender_connection()
    return conn.send_command("remove_modifier", {
        "object_name": Validator.validate_name(object_name),
        "modifier_name": Validator.validate_name(modifier_name),
    })


@mcp.tool()
def reorder_modifier(object_name: str, modifier_name: str, new_index: int) -> dict:
    """Move a modifier to a specific position in the stack.

    Args:
        object_name: Target object.
        modifier_name: Modifier to move.
        new_index: Target position (0-based).
    """
    conn = get_blender_connection()
    return conn.send_command("reorder_modifier", {
        "object_name": Validator.validate_name(object_name),
        "modifier_name": Validator.validate_name(modifier_name),
        "new_index": Validator.validate_int(new_index, 0, 100),
    })


@mcp.tool()
def boolean_operation(
    object_name: str,
    target_name: str,
    operation: str = "DIFFERENCE",
) -> dict:
    """Perform a boolean operation between two objects.

    Args:
        object_name: Object to modify.
        target_name: Object to use as boolean operand.
        operation: UNION, INTERSECT, or DIFFERENCE.
    """
    conn = get_blender_connection()
    return conn.send_command("boolean_operation", {
        "object_name": Validator.validate_name(object_name),
        "target_name": Validator.validate_name(target_name),
        "operation": Validator.validate_enum(operation, "bool_operation"),
    })


@mcp.tool()
def extrude_faces(object_name: str, distance: float = 0.0) -> dict:
    """Extrude selected faces of a mesh object (must be in edit mode).

    Args:
        object_name: Object name.
        distance: Extrusion distance (0 for manual manipulation).
    """
    conn = get_blender_connection()
    return conn.send_command("extrude_faces", {
        "object_name": Validator.validate_name(object_name),
        "distance": Validator.validate_float(distance),
    })


@mcp.tool()
def inset_faces(object_name: str, thickness: float = 0.1, use_boundary: bool = True) -> dict:
    """Inset selected faces of a mesh.

    Args:
        object_name: Object name.
        thickness: Inset thickness.
        use_boundary: Also inset boundary edges.
    """
    conn = get_blender_connection()
    return conn.send_command("inset_faces", {
        "object_name": Validator.validate_name(object_name),
        "thickness": Validator.validate_float(thickness, 0.001, 100),
        "use_boundary": use_boundary,
    })


@mcp.tool()
def bevel_edges(object_name: str, width: float = 0.1, segments: int = 1) -> dict:
    """Bevel selected edges of a mesh.

    Args:
        object_name: Object name.
        width: Bevel width.
        segments: Number of segments (1 = flat bevel).
    """
    conn = get_blender_connection()
    return conn.send_command("bevel_edges", {
        "object_name": Validator.validate_name(object_name),
        "width": Validator.validate_float(width, 0.001, 100),
        "segments": Validator.validate_int(segments, 1, 32),
    })


@mcp.tool()
def loop_cut(object_name: str, number_cuts: int = 1, axis: str = "X") -> dict:
    """Add loop cuts to a mesh.

    Args:
        object_name: Object name.
        number_cuts: Number of cuts.
        axis: X, Y, or Z axis.
    """
    conn = get_blender_connection()
    return conn.send_command("loop_cut", {
        "object_name": Validator.validate_name(object_name),
        "number_cuts": Validator.validate_int(number_cuts, 1, 50),
        "axis": Validator.validate_enum(axis, "axis"),
    })


@mcp.tool()
def subdivide_mesh(object_name: str, cuts: int = 1, smooth: float = 0.0) -> dict:
    """Subdivide selected mesh geometry.

    Args:
        object_name: Object name.
        cuts: Number of subdivision cuts.
        smooth: Smooth factor (0-1).
    """
    conn = get_blender_connection()
    return conn.send_command("subdivide_mesh", {
        "object_name": Validator.validate_name(object_name),
        "cuts": Validator.validate_int(cuts, 1, 10),
        "smooth": Validator.validate_percentage(smooth) / 100.0,
    })


@mcp.tool()
def merge_vertices(object_name: str, distance: float = 0.001) -> dict:
    """Merge vertices by distance (remove doubles).

    Args:
        object_name: Object name.
        distance: Merge distance threshold.
    """
    conn = get_blender_connection()
    return conn.send_command("merge_vertices", {
        "object_name": Validator.validate_name(object_name),
        "distance": Validator.validate_float(distance, 0.0001, 10),
    })


@mcp.tool()
def flip_normals(object_name: str) -> dict:
    """Flip normals of selected faces.

    Args:
        object_name: Object name.
    """
    conn = get_blender_connection()
    return conn.send_command("flip_normals", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def recalculate_normals(object_name: str, outside: bool = True) -> dict:
    """Recalculate normals of a mesh.

    Args:
        object_name: Object name.
        outside: If True, normals point outward.
    """
    conn = get_blender_connection()
    return conn.send_command("recalculate_normals", {
        "object_name": Validator.validate_name(object_name),
        "outside": outside,
    })
