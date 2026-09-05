"""Mesh editing tools — vertex, edge, and face-level operations."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def edit_mesh_vertices(
    object_name: str,
    action: str = "move",
    vertices: list[int] = None,
    offset: list[float] = None,
) -> dict:
    """Edit mesh vertices at the element level.

    Args:
        object_name: Target mesh object.
        action: move, delete, smooth, or collapse.
        vertices: List of vertex indices to operate on (None = selected).
        offset: [x, y, z] offset for move action.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "action": action.lower(),
    }
    if vertices is not None:
        params["vertices"] = vertices
    if offset is not None:
        params["offset"] = Validator.validate_vector(offset)
    return conn.send_command("edit_mesh_vertices", params)


@mcp.tool()
def edit_mesh_edges(
    object_name: str,
    action: str = "select",
    edges: list[int] = None,
) -> dict:
    """Edit mesh edges.

    Args:
        object_name: Target mesh object.
        action: select, deselect, mark_seam, clear_seam, mark_sharp, crease.
        edges: List of edge indices (None = selected).
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "action": action.lower(),
    }
    if edges is not None:
        params["edges"] = edges
    return conn.send_command("edit_mesh_edges", params)


@mcp.tool()
def edit_mesh_faces(
    object_name: str,
    action: str = "select",
    faces: list[int] = None,
) -> dict:
    """Edit mesh faces.

    Args:
        object_name: Target mesh object.
        action: select, deselect, delete, fill, grid_fill, triangulate, poke.
        faces: List of face indices (None = selected).
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "action": action.lower(),
    }
    if faces is not None:
        params["faces"] = faces
    return conn.send_command("edit_mesh_faces", params)


@mcp.tool()
def create_vertex_group(object_name: str, group_name: str) -> dict:
    """Create a new vertex group on a mesh object.

    Args:
        object_name: Target object.
        group_name: Name for the vertex group.
    """
    conn = get_blender_connection()
    return conn.send_command("create_vertex_group", {
        "object_name": Validator.validate_name(object_name),
        "group_name": Validator.validate_name(group_name),
    })


@mcp.tool()
def assign_vertex_group(
    object_name: str,
    group_name: str,
    vertices: list[int],
    weight: float = 1.0,
) -> dict:
    """Assign vertices to a vertex group with a specific weight.

    Args:
        object_name: Target object.
        group_name: Vertex group name.
        vertices: Vertex indices to assign.
        weight: Weight value (0.0 - 1.0).
    """
    conn = get_blender_connection()
    return conn.send_command("assign_vertex_group", {
        "object_name": Validator.validate_name(object_name),
        "group_name": Validator.validate_name(group_name),
        "vertices": vertices,
        "weight": max(0.0, min(1.0, float(weight))),
    })


@mcp.tool()
def separate_by_material(object_name: str) -> dict:
    """Separate a mesh object into parts by material assignment.

    Args:
        object_name: Object to separate.
    """
    conn = get_blender_connection()
    return conn.send_command("separate_by_material", {
        "object_name": Validator.validate_name(object_name),
    })


@mcp.tool()
def separate_by_loose(object_name: str) -> dict:
    """Separate a mesh into disconnected parts.

    Args:
        object_name: Object to separate.
    """
    conn = get_blender_connection()
    return conn.send_command("separate_by_loose", {
        "object_name": Validator.validate_name(object_name),
    })


@mcp.tool()
def smooth_vertices(object_name: str, factor: float = 0.5, iterations: int = 1) -> dict:
    """Smooth selected vertices.

    Args:
        object_name: Target object.
        factor: Smoothing factor (0-1).
        iterations: Number of smoothing iterations.
    """
    conn = get_blender_connection()
    return conn.send_command("smooth_vertices", {
        "object_name": Validator.validate_name(object_name),
        "factor": Validator.validate_percentage(factor) / 100.0,
        "iterations": Validator.validate_int(iterations, 1, 100),
    })


@mcp.tool()
def tri_to_quad(object_name: str, angle_limit: float = 0.698) -> dict:
    """Convert triangles to quads.

    Args:
        object_name: Target object.
        angle_limit: Angle limit in radians.
    """
    conn = get_blender_connection()
    return conn.send_command("tri_to_quad", {
        "object_name": Validator.validate_name(object_name),
        "angle_limit": Validator.validate_float(angle_limit, 0, 3.14159),
    })


@mcp.tool()
def limited_dissolve(object_name: str, angle_limit: float = 0.087) -> dict:
    """Dissolve geometry based on angle threshold.

    Args:
        object_name: Target object.
        angle_limit: Angle threshold in radians.
    """
    conn = get_blender_connection()
    return conn.send_command("limited_dissolve", {
        "object_name": Validator.validate_name(object_name),
        "angle_limit": Validator.validate_float(angle_limit, 0, 3.14159),
    })
