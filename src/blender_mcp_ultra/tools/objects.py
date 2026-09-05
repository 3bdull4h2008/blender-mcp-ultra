"""Object management tools — create, delete, duplicate, organize objects."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_object(
    object_type: str = "MESH",
    name: str = "Object",
    location: list[float] = None,
    rotation: list[float] = None,
    scale: list[float] = None,
    **kwargs,
) -> dict:
    """Create a new object of any type with optional transform.

    Args:
        object_type: MESH, CURVE, SURFACE, META, TEXT, ARMATURE, LATTICE, EMPTY, CAMERA, LIGHT, etc.
        name: Name for the new object.
        location: [x, y, z] world position.
        rotation: [x, y, z] Euler rotation in radians.
        scale: [x, y, z] scale factors.
    """
    conn = get_blender_connection()
    params = {
        "object_type": Validator.validate_enum(object_type, "object_type"),
        "name": Validator.validate_name(name),
    }
    if location:
        params["location"] = Validator.validate_vector(location)
    if rotation:
        params["rotation"] = Validator.validate_vector(rotation)
    if scale:
        params["scale"] = Validator.validate_vector(scale)
    params.update(kwargs)
    return conn.send_command("create_object", params)


@mcp.tool()
def delete_object(name: str) -> dict:
    """Delete an object by name.

    Args:
        name: Name of the object to delete.
    """
    conn = get_blender_connection()
    return conn.send_command("delete_object", {"name": Validator.validate_name(name)})


@mcp.tool()
def duplicate_object(name: str, new_name: str = "") -> dict:
    """Duplicate an object with all its data.

    Args:
        name: Name of the object to duplicate.
        new_name: Optional name for the duplicate.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if new_name:
        params["new_name"] = Validator.validate_name(new_name)
    return conn.send_command("duplicate_object", params)


@mcp.tool()
def rename_object(name: str, new_name: str) -> dict:
    """Rename an object.

    Args:
        name: Current name of the object.
        new_name: New name for the object.
    """
    conn = get_blender_connection()
    return conn.send_command("rename_object", {
        "name": Validator.validate_name(name),
        "new_name": Validator.validate_name(new_name),
    })


@mcp.tool()
def select_objects(names: list[str], replace: bool = True) -> dict:
    """Select one or more objects by name.

    Args:
        names: List of object names to select.
        replace: If True, deselect all others first.
    """
    conn = get_blender_connection()
    return conn.send_command("select_objects", {
        "names": [Validator.validate_name(n) for n in names],
        "replace": replace,
    })


@mcp.tool()
def set_object_visibility(name: str, visible: bool = True, hide_render: bool = False) -> dict:
    """Set object viewport and/or render visibility.

    Args:
        name: Object name.
        visible: Viewport visibility.
        hide_render: Render visibility.
    """
    conn = get_blender_connection()
    return conn.send_command("set_object_visibility", {
        "name": Validator.validate_name(name),
        "visible": visible,
        "hide_render": hide_render,
    })


@mcp.tool()
def parent_objects(child: str, parent: str, keep_transform: bool = True) -> dict:
    """Set parent-child relationship between objects.

    Args:
        child: Name of the child object.
        parent: Name of the parent object.
        keep_transform: If True, maintain the child's current world transform.
    """
    conn = get_blender_connection()
    return conn.send_command("parent_objects", {
        "child": Validator.validate_name(child),
        "parent": Validator.validate_name(parent),
        "keep_transform": keep_transform,
    })


@mcp.tool()
def join_objects(names: list[str]) -> dict:
    """Join multiple objects into a single mesh.

    Args:
        names: List of object names to join. First object becomes the active.
    """
    conn = get_blender_connection()
    return conn.send_command("join_objects", {
        "names": [Validator.validate_name(n) for n in names],
    })


@mcp.tool()
def set_origin(name: str, origin_type: str = "GEOMETRY") -> dict:
    """Set the origin of an object.

    Args:
        name: Object name.
        origin_type: GEOMETRY, CURSOR, CENTER_OF_MASS, or CENTER_OF_VOLUME.
    """
    conn = get_blender_connection()
    return conn.send_command("set_origin", {
        "name": Validator.validate_name(name),
        "origin_type": origin_type.upper(),
    })


@mcp.tool()
def convert_object(name: str, target_type: str = "MESH") -> dict:
    """Convert an object to a different type (e.g., curve to mesh).

    Args:
        name: Object name.
        target_type: Target type (MESH, CURVE, SURFACE, etc.).
    """
    conn = get_blender_connection()
    return conn.send_command("convert_object", {
        "name": Validator.validate_name(name),
        "target_type": Validator.validate_enum(target_type, "object_type"),
    })


@mcp.tool()
def shade_object(name: str, shading: str = "SMOOTH") -> dict:
    """Set shading mode for an object.

    Args:
        name: Object name.
        shading: FLAT or SMOOTH.
    """
    conn = get_blender_connection()
    return conn.send_command("shade_object", {
        "name": Validator.validate_name(name),
        "shading": Validator.validate_enum(shading, "shading"),
    })
