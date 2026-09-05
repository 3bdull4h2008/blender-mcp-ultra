"""Lighting tools — create, configure lights and environment."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_light(
    name: str = "Light",
    light_type: str = "POINT",
    location: list[float] = None,
    energy: float = 1000.0,
    color: list[float] = None,
    radius: float = 0.0,
) -> dict:
    """Create a light source.

    Args:
        name: Light name.
        light_type: POINT, SUN, SPOT, or AREA.
        location: [x, y, z] position.
        energy: Light power in watts.
        color: [R, G, B] light color.
        radius: Soft shadow radius.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "light_type": Validator.validate_enum(light_type, "light_type"),
        "energy": Validator.validate_float(energy, 0, 1000000),
        "radius": Validator.validate_float(radius, 0, 100),
    }
    if location:
        params["location"] = Validator.validate_vector(location)
    if color:
        params["color"] = Validator.validate_color(color)
    return conn.send_command("create_light", params)


@mcp.tool()
def configure_light(
    name: str,
    energy: float = None,
    color: list[float] = None,
    radius: float = None,
    spot_angle: float = None,
    shadow_soft_size: float = None,
) -> dict:
    """Configure an existing light's properties.

    Args:
        name: Light object name.
        energy: Power in watts.
        color: [R, G, B] light color.
        radius: Soft shadow radius.
        spot_angle: Spot cone angle in radians (spot lights only).
        shadow_soft_size: Shadow soft size.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if energy is not None:
        params["energy"] = Validator.validate_float(energy, 0, 1000000)
    if color is not None:
        params["color"] = Validator.validate_color(color)
    if radius is not None:
        params["radius"] = Validator.validate_float(radius, 0, 100)
    if spot_angle is not None:
        params["spot_angle"] = Validator.validate_float(spot_angle, 0, 3.14159)
    if shadow_soft_size is not None:
        params["shadow_soft_size"] = Validator.validate_float(shadow_soft_size, 0, 100)
    return conn.send_command("configure_light", params)


@mcp.tool()
def setup_three_point_lighting(
    key_energy: float = 1000.0,
    fill_energy: float = 300.0,
    rim_energy: float = 500.0,
    key_color: list[float] = None,
    fill_color: list[float] = None,
    rim_color: list[float] = None,
    distance: float = 5.0,
) -> dict:
    """Set up professional three-point lighting (key, fill, rim).

    Args:
        key_energy: Key light power (watts). Typically 1000W.
        fill_energy: Fill light power. Typically 1/3 of key.
        rim_energy: Rim/back light power. Typically 1/2 of key.
        key_color: [R, G, B] key light color.
        fill_color: [R, G, B] fill light color.
        rim_color: [R, G, B] rim light color.
        distance: Distance from origin.
    """
    conn = get_blender_connection()
    params = {
        "key_energy": Validator.validate_float(key_energy, 0, 1000000),
        "fill_energy": Validator.validate_float(fill_energy, 0, 1000000),
        "rim_energy": Validator.validate_float(rim_energy, 0, 1000000),
        "distance": Validator.validate_float(distance, 0.1, 1000),
    }
    if key_color:
        params["key_color"] = Validator.validate_color(key_color)
    if fill_color:
        params["fill_color"] = Validator.validate_color(fill_color)
    if rim_color:
        params["rim_color"] = Validator.validate_color(rim_color)
    return conn.send_command("setup_three_point_lighting", params)


@mcp.tool()
def setup_hdri_lighting(
    hdri_path: str = "",
    strength: float = 1.0,
    rotation: float = 0.0,
) -> dict:
    """Set up HDRI environment lighting.

    Args:
        hdri_path: Path to HDRI file. If empty, uses a default gradient.
        strength: Environment strength.
        rotation: Rotation in radians.
    """
    conn = get_blender_connection()
    params = {
        "strength": Validator.validate_float(strength, 0, 100),
        "rotation": Validator.validate_float(rotation),
    }
    if hdri_path:
        params["hdri_path"] = Validator.validate_path(hdri_path)
    return conn.send_command("setup_hdri_lighting", params)


@mcp.tool()
def setup_studio_lighting(
    style: str = "STUDIO",
    key_energy: float = 1000.0,
) -> dict:
    """Set up preset studio lighting configurations.

    Args:
        style: STUDIO, PORTRAIT, PRODUCT, DRAMATIC, or SOFT.
        key_energy: Key light power.
    """
    conn = get_blender_connection()
    return conn.send_command("setup_studio_lighting", {
        "style": style.upper(),
        "key_energy": Validator.validate_float(key_energy, 0, 1000000),
    })


@mcp.tool()
def set_world_environment(
    color: list[float] = None,
    strength: float = 1.0,
    use_nodes: bool = True,
) -> dict:
    """Set world/environment background.

    Args:
        color: [R, G, B] background color.
        strength: Environment strength.
        use_nodes: Use shader nodes for environment.
    """
    conn = get_blender_connection()
    params = {
        "strength": Validator.validate_float(strength, 0, 100),
        "use_nodes": use_nodes,
    }
    if color:
        params["color"] = Validator.validate_color(color)
    return conn.send_command("set_world_environment", params)


@mcp.tool()
def list_lights() -> dict:
    """List all lights in the scene with their types, positions, and energy values."""
    conn = get_blender_connection()
    return conn.send_command("list_lights")
