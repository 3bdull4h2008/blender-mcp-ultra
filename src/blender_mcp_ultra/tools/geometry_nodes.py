"""Geometry Nodes tools — procedural generation via node-based systems."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def add_geometry_nodes_modifier(
    object_name: str,
    node_group_name: str = "GeometryNodes",
) -> dict:
    """Add a geometry nodes modifier to an object.

    Args:
        object_name: Target object.
        node_group_name: Name for the node group.
    """
    conn = get_blender_connection()
    return conn.send_command("add_geometry_nodes_modifier", {
        "object_name": Validator.validate_name(object_name),
        "node_group_name": Validator.validate_name(node_group_name),
    })


@mcp.tool()
def add_geometry_node(
    node_group_name: str,
    node_type: str,
    location: list[float] = None,
) -> dict:
    """Add a node to a geometry node tree.

    Args:
        node_group_name: Node group name.
        node_type: Node type (e.g., 'MeshPrimitiveCube', 'InstanceOnPoints', 'SetPosition').
        location: [x, y] position in the node editor.
    """
    conn = get_blender_connection()
    params = {
        "node_group_name": Validator.validate_name(node_group_name),
        "node_type": node_type,
    }
    if location:
        params["location"] = Validator.validate_vector(location, 2)
    return conn.send_command("add_geometry_node", params)


@mcp.tool()
def connect_geometry_nodes(
    node_group_name: str,
    from_node: str,
    from_socket: str,
    to_node: str,
    to_socket: str,
) -> dict:
    """Connect two nodes in a geometry node tree.

    Args:
        node_group_name: Node group name.
        from_node: Source node name.
        from_socket: Source socket name.
        to_node: Target node name.
        to_socket: Target socket name.
    """
    conn = get_blender_connection()
    return conn.send_command("connect_geometry_nodes", {
        "node_group_name": Validator.validate_name(node_group_name),
        "from_node": from_node,
        "from_socket": from_socket,
        "to_node": to_node,
        "to_socket": to_socket,
    })


@mcp.tool()
def create_procedural_distribution(
    object_name: str,
    instance_object: str = "",
    count: int = 100,
    distribution: str = "RANDOM",
    seed: int = 0,
) -> dict:
    """Set up points-on-faces distribution via geometry nodes.

    Args:
        object_name: Target object to distribute on.
        instance_object: Object to instance on each point. Empty = just points.
        count: Number of instances.
        distribution: RANDOM, POISSON_DISK, or GRID.
        seed: Random seed.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "count": Validator.validate_int(count, 1, 1000000),
        "distribution": distribution.upper(),
        "seed": Validator.validate_int(seed, 0, 1000000),
    }
    if instance_object:
        params["instance_object"] = Validator.validate_name(instance_object)
    return conn.send_command("create_procedural_distribution", params)
