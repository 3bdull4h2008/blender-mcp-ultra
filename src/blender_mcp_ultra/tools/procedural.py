"""Procedural generation tools — generate meshes, trees, terrains, and objects."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_terrain(
    name: str = "Terrain",
    size: float = 10.0,
    subdivisions: int = 128,
    height: float = 1.0,
    seed: int = 0,
    noise_scale: float = 2.0,
) -> dict:
    """Generate a procedural terrain mesh.

    Args:
        name: Object name.
        size: Grid size.
        subdivisions: Number of subdivisions.
        height: Maximum height.
        seed: Random seed.
        noise_scale: Noise scale factor.
    """
    conn = get_blender_connection()
    return conn.send_command("create_terrain", {
        "name": Validator.validate_name(name),
        "size": Validator.validate_float(size, 0.1, 1000),
        "subdivisions": Validator.validate_int(subdivisions, 4, 1024),
        "height": Validator.validate_float(height, 0.01, 100),
        "seed": Validator.validate_int(seed, 0, 1000000),
        "noise_scale": Validator.validate_float(noise_scale, 0.01, 100),
    })


@mcp.tool()
def create_tree(
    name: str = "Tree",
    trunk_height: float = 3.0,
    trunk_radius: float = 0.15,
    branch_levels: int = 3,
    leaves_per_branch: int = 5,
    seed: int = 0,
) -> dict:
    """Generate a procedural tree with trunk, branches, and leaves.

    Args:
        name: Object name.
        trunk_height: Height of the trunk.
        trunk_radius: Radius of the trunk.
        branch_levels: Number of branching levels.
        leaves_per_branch: Leaves per branch.
        seed: Random seed.
    """
    conn = get_blender_connection()
    return conn.send_command("create_tree", {
        "name": Validator.validate_name(name),
        "trunk_height": Validator.validate_float(trunk_height, 0.1, 100),
        "trunk_radius": Validator.validate_float(trunk_radius, 0.01, 10),
        "branch_levels": Validator.validate_int(branch_levels, 0, 6),
        "leaves_per_branch": Validator.validate_int(leaves_per_branch, 0, 20),
        "seed": Validator.validate_int(seed, 0, 1000000),
    })


@mcp.tool()
def create_rock(
    name: str = "Rock",
    size: float = 1.0,
    detail: float = 0.5,
    roughness: float = 0.8,
    seed: int = 0,
) -> dict:
    """Generate a procedural rock.

    Args:
        name: Object name.
        size: Rock size.
        detail: Surface detail level (0-1).
        roughness: Surface roughness.
        seed: Random seed.
    """
    conn = get_blender_connection()
    return conn.send_command("create_rock", {
        "name": Validator.validate_name(name),
        "size": Validator.validate_float(size, 0.01, 100),
        "detail": Validator.validate_percentage(detail) / 100.0,
        "roughness": Validator.validate_percentage(roughness) / 100.0,
        "seed": Validator.validate_int(seed, 0, 1000000),
    })


@mcp.tool()
def create_particle_field(
    name: str = "ParticleField",
    count: int = 100,
    size: float = 5.0,
    particle_size: float = 0.1,
    seed: int = 0,
) -> dict:
    """Generate a field of scattered particles/objects.

    Args:
        name: Object name.
        count: Number of particles.
        size: Field size.
        particle_size: Individual particle size.
        seed: Random seed.
    """
    conn = get_blender_connection()
    return conn.send_command("create_particle_field", {
        "name": Validator.validate_name(name),
        "count": Validator.validate_int(count, 1, 100000),
        "size": Validator.validate_float(size, 0.1, 1000),
        "particle_size": Validator.validate_float(particle_size, 0.001, 100),
        "seed": Validator.validate_int(seed, 0, 1000000),
    })
