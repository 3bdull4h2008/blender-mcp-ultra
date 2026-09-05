"""Material and shader tools — create, assign, configure materials and nodes."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_material(name: str = "Material", color: list[float] = None, metallic: float = 0.0, roughness: float = 0.5) -> dict:
    """Create a new Principled BSDF material.

    Args:
        name: Material name.
        color: [R, G, B, A] base color (0-1).
        metallic: Metallic value (0-1).
        roughness: Roughness value (0-1).
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "metallic": Validator.validate_percentage(metallic) / 100.0,
        "roughness": Validator.validate_percentage(roughness) / 100.0,
    }
    if color:
        params["color"] = Validator.validate_color(color)
    return conn.send_command("create_material", params)


@mcp.tool()
def assign_material(object_name: str, material_name: str, slot: int = 0) -> dict:
    """Assign a material to an object's material slot.

    Args:
        object_name: Target object.
        material_name: Material to assign.
        slot: Material slot index.
    """
    conn = get_blender_connection()
    return conn.send_command("assign_material", {
        "object_name": Validator.validate_name(object_name),
        "material_name": Validator.validate_name(material_name),
        "slot": Validator.validate_int(slot, 0, 32),
    })


@mcp.tool()
def delete_material(object_name: str, slot: int = 0) -> dict:
    """Remove material from an object's slot.

    Args:
        object_name: Target object.
        slot: Material slot index.
    """
    conn = get_blender_connection()
    return conn.send_command("delete_material", {
        "object_name": Validator.validate_name(object_name),
        "slot": Validator.validate_int(slot, 0, 32),
    })


@mcp.tool()
def set_material_property(material_name: str, property_name: str, value) -> dict:
    """Set a property on a material's Principled BSDF node.

    Args:
        material_name: Target material.
        property_name: Node input name (e.g., 'Base Color', 'Metallic', 'Roughness').
        value: The value to set.
    """
    conn = get_blender_connection()
    return conn.send_command("set_material_property", {
        "material_name": Validator.validate_name(material_name),
        "property_name": property_name,
        "value": value,
    })


@mcp.tool()
def create_procedural_material(
    name: str = "Procedural",
    pattern: str = "NOISE",
    color1: list[float] = None,
    color2: list[float] = None,
    scale: float = 1.0,
    detail: float = 6.0,
    roughness: float = 0.5,
) -> dict:
    """Create a complete procedural material with node graph in one call.

    Creates coordinate mapping, texture node, color ramp, and Principled BSDF.

    Args:
        name: Material name.
        pattern: NOISE, VORONOI, MUSGRAVE, WAVY, MAGIC, checker, marble, wood, cloud, gradient, veins, plasma.
        color1: First color [R, G, B].
        color2: Second color [R, G, B].
        scale: Texture scale.
        detail: Texture detail level.
        roughness: Surface roughness.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "pattern": pattern.lower(),
        "scale": Validator.validate_float(scale, 0.01, 1000),
        "detail": Validator.validate_float(detail, 0, 16),
        "roughness": Validator.validate_percentage(roughness) / 100.0,
    }
    if color1:
        params["color1"] = Validator.validate_color(color1)
    if color2:
        params["color2"] = Validator.validate_color(color2)
    return conn.send_command("create_procedural_material", params)


@mcp.tool()
def add_shader_node(
    material_name: str,
    node_type: str,
    location: list[float] = None,
    name: str = "",
) -> dict:
    """Add a shader node to a material's node tree.

    Args:
        material_name: Target material.
        node_type: Shader node type (e.g., 'TEX_NOISE', 'TEX_VORONOI', 'MIXRGB', 'VALUE').
        location: [x, y] position in the node editor.
        name: Optional node label.
    """
    conn = get_blender_connection()
    params = {
        "material_name": Validator.validate_name(material_name),
        "node_type": node_type,
    }
    if location:
        params["location"] = Validator.validate_vector(location, 2)
    if name:
        params["name"] = Validator.validate_name(name)
    return conn.send_command("add_shader_node", params)


@mcp.tool()
def connect_shader_nodes(
    material_name: str,
    from_node: str,
    from_socket: str,
    to_node: str,
    to_socket: str,
) -> dict:
    """Connect two shader nodes in a material's node tree.

    Args:
        material_name: Target material.
        from_node: Source node name/label.
        from_socket: Source socket name.
        to_node: Target node name/label.
        to_socket: Target socket name.
    """
    conn = get_blender_connection()
    return conn.send_command("connect_shader_nodes", {
        "material_name": Validator.validate_name(material_name),
        "from_node": from_node,
        "from_socket": from_socket,
        "to_node": to_node,
        "to_socket": to_socket,
    })


@mcp.tool()
def set_shader_node_value(
    material_name: str,
    node_name: str,
    value,
) -> dict:
    """Set the value of a shader node input.

    Args:
        material_name: Target material.
        node_name: Node name/label.
        value: Value to set.
    """
    conn = get_blender_connection()
    return conn.send_command("set_shader_node_value", {
        "material_name": Validator.validate_name(material_name),
        "node_name": node_name,
        "value": value,
    })


@mcp.tool()
def apply_image_texture(
    object_name: str,
    image_path: str,
    material_name: str = "",
) -> dict:
    """Apply an image texture to an object.

    Args:
        object_name: Target object.
        image_path: Path to the image file.
        material_name: Optional existing material to add texture to.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "image_path": Validator.validate_path(image_path),
    }
    if material_name:
        params["material_name"] = Validator.validate_name(material_name)
    return conn.send_command("apply_image_texture", params)


@mcp.tool()
def list_materials() -> dict:
    """List all materials in the current blend file with their names and usage counts."""
    conn = get_blender_connection()
    return conn.send_command("list_materials")
