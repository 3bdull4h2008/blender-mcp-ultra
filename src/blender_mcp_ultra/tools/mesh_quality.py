"""Mesh quality analysis — detect defects, measure topology, production readiness."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def analyze_mesh_quality(object_name: str) -> dict:
    """Analyze mesh for defects: non-manifold edges, loose vertices, zero-area faces,
    duplicate vertices, wire edges, and twisted faces.

    Returns a structured defect report with counts and affected element indices.
    """
    conn = get_blender_connection()
    return conn.send_command("analyze_mesh_quality", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def get_mesh_statistics(object_name: str) -> dict:
    """Get detailed mesh statistics: vertex/edge/face counts, triangle count,
    ngon count, volume, surface area, bounding box dimensions.
    """
    conn = get_blender_connection()
    return conn.send_command("get_mesh_statistics", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def check_manifold(object_name: str) -> dict:
    """Check if mesh is manifold (watertight).

    Returns is_manifold bool, non_manifold_edge_count, and boundary_edge_count.
    """
    conn = get_blender_connection()
    return conn.send_command("check_manifold", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def get_geometry_complexity(object_name: str) -> dict:
    """Get geometry complexity metrics: triangle count, vertex count, ngon count,
    and complexity tier (simple/moderate/complex/high-poly).
    """
    conn = get_blender_connection()
    return conn.send_command("get_geometry_complexity", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def check_production_readiness(object_name: str) -> dict:
    """Full production readiness audit: manifold geometry, UV maps, materials,
    naming conventions, origin alignment. Returns a score 0-100 with detailed breakdown.
    """
    conn = get_blender_connection()
    return conn.send_command("check_production_readiness", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def find_duplicates(object_name: str, distance: float = 0.001) -> dict:
    """Find duplicate vertices within a distance threshold.

    Args:
        object_name: Target object.
        distance: Distance threshold for duplicate detection.
    """
    conn = get_blender_connection()
    return conn.send_command("find_duplicates", {
        "object_name": Validator.validate_name(object_name),
        "distance": Validator.validate_float(distance, 0.0001, 10),
    })


@mcp.tool()
def fix_mesh_defects(object_name: str, fix_manifold: bool = True, merge_distance: float = 0.001) -> dict:
    """Automatically fix common mesh defects.

    Args:
        object_name: Target object.
        fix_manifold: Fix non-manifold geometry.
        merge_distance: Distance for merging duplicate vertices.
    """
    conn = get_blender_connection()
    return conn.send_command("fix_mesh_defects", {
        "object_name": Validator.validate_name(object_name),
        "fix_manifold": fix_manifold,
        "merge_distance": Validator.validate_float(merge_distance, 0.0001, 1),
    })
