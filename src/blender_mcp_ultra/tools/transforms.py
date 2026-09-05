"""Transform tools — move, rotate, scale objects with precision."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def set_object_transform(
    name: str,
    location: list[float] | None = None,
    rotation: list[float] | None = None,
    scale: list[float] | None = None,
    space: str = "WORLD",
) -> dict:
    """Set world/local transform of an object. Only provided channels are modified.

    Args:
        name: Object name.
        location: [x, y, z] position.
        rotation: [x, y, z] Euler rotation in radians.
        scale: [x, y, z] scale factors.
        space: WORLD or LOCAL coordinate space.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "space": Validator.validate_enum(space, "transform_space"),
    }
    if location is not None:
        params["location"] = Validator.validate_vector(location)
    if rotation is not None:
        params["rotation"] = Validator.validate_vector(rotation)
    if scale is not None:
        params["scale"] = Validator.validate_vector(scale)
    return conn.send_command("set_object_transform", params)


@mcp.tool()
def move_object(name: str, x: float = 0, y: float = 0, z: float = 0, space: str = "WORLD") -> dict:
    """Move an object by delta in world or local space.

    Args:
        name: Object name.
        x, y, z: Translation delta.
        space: WORLD or LOCAL.
    """
    conn = get_blender_connection()
    return conn.send_command("move_object", {
        "name": Validator.validate_name(name),
        "x": Validator.validate_float(x),
        "y": Validator.validate_float(y),
        "z": Validator.validate_float(z),
        "space": Validator.validate_enum(space, "transform_space"),
    })


@mcp.tool()
def rotate_object(name: str, x: float = 0, y: float = 0, z: float = 0, space: str = "WORLD") -> dict:
    """Rotate an object by delta radians in world or local space.

    Args:
        name: Object name.
        x, y, z: Rotation delta in radians.
        space: WORLD or LOCAL.
    """
    conn = get_blender_connection()
    return conn.send_command("rotate_object", {
        "name": Validator.validate_name(name),
        "x": Validator.validate_float(x),
        "y": Validator.validate_float(y),
        "z": Validator.validate_float(z),
        "space": Validator.validate_enum(space, "transform_space"),
    })


@mcp.tool()
def scale_object(name: str, x: float = 1.0, y: float = 1.0, z: float = 1.0) -> dict:
    """Scale an object by factors.

    Args:
        name: Object name.
        x, y, z: Scale factors (1.0 = no change).
    """
    conn = get_blender_connection()
    return conn.send_command("scale_object", {
        "name": Validator.validate_name(name),
        "x": Validator.validate_float(x, 0.001, 10000),
        "y": Validator.validate_float(y, 0.001, 10000),
        "z": Validator.validate_float(z, 0.001, 10000),
    })


@mcp.tool()
def apply_transform(name: str, location: bool = True, rotation: bool = True, scale: bool = True) -> dict:
    """Apply (bake) transforms — resets values to identity while keeping world position.

    Args:
        name: Object name.
        location: Apply location.
        rotation: Apply rotation.
        scale: Apply scale.
    """
    conn = get_blender_connection()
    return conn.send_command("apply_transform", {
        "name": Validator.validate_name(name),
        "location": location,
        "rotation": rotation,
        "scale": scale,
    })


@mcp.tool()
def get_local_transforms(name: str) -> dict:
    """Get the local (parent-relative) transforms of an object.

    Args:
        name: Object name.
    """
    conn = get_blender_connection()
    return conn.send_command("get_local_transforms", {"name": Validator.validate_name(name)})


@mcp.tool()
def align_object(
    name: str,
    target: str,
    align_location: bool = True,
    align_rotation: bool = False,
    align_scale: bool = False,
) -> dict:
    """Align one object's transform to another.

    Args:
        name: Object to align.
        target: Reference object.
        align_location: Match position.
        align_rotation: Match rotation.
        align_scale: Match scale.
    """
    conn = get_blender_connection()
    return conn.send_command("align_object", {
        "name": Validator.validate_name(name),
        "target": Validator.validate_name(target),
        "align_location": align_location,
        "align_rotation": align_rotation,
        "align_scale": align_scale,
    })


@mcp.tool()
def snap_to_cursor(name: str, cursor_location: list[float] = None) -> dict:
    """Snap an object's origin to the 3D cursor or a specific location.

    Args:
        name: Object name.
        cursor_location: Optional [x, y, z] to set cursor first.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if cursor_location:
        params["cursor_location"] = Validator.validate_vector(cursor_location)
    return conn.send_command("snap_to_cursor", params)
