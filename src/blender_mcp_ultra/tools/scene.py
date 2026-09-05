"""Scene management tools — inspect, create, configure Blender scenes."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def get_scene_info() -> dict:
    """Get comprehensive scene information: objects, hierarchy, frame range, render settings.

    Returns scene name, active object, object count with type breakdown,
    full object list with transforms, collection hierarchy, and render config.
    """
    conn = get_blender_connection()
    return conn.send_command("get_scene_info")


@mcp.tool()
def list_objects(
    object_type: str = "ALL",
    include_hidden: bool = False,
    collection: str | None = None,
) -> dict:
    """List all objects in the scene with their types, locations, and visibility.

    Args:
        object_type: Filter by type: ALL, MESH, CURVE, LIGHT, CAMERA, ARMATURE, EMPTY, etc.
        include_hidden: If True, include hidden objects.
        collection: Optional collection name to filter by.
    """
    conn = get_blender_connection()
    params = {"object_type": object_type, "include_hidden": include_hidden}
    if collection:
        params["collection"] = Validator.validate_name(collection)
    return conn.send_command("list_objects", params)


@mcp.tool()
def get_object_info(object_name: str) -> dict:
    """Get detailed information about a specific object: transforms, mesh stats,
    materials, modifiers, constraints, vertex groups, and shape keys.

    Args:
        object_name: Name of the object to inspect.
    """
    conn = get_blender_connection()
    return conn.send_command("get_object_info", {"object_name": Validator.validate_name(object_name)})


@mcp.tool()
def create_scene(name: str = "Scene", copy_current: bool = False) -> dict:
    """Create a new scene.

    Args:
        name: Name for the new scene.
        copy_current: If True, copy the current scene's settings.
    """
    conn = get_blender_connection()
    return conn.send_command("create_scene", {
        "name": Validator.validate_name(name),
        "copy_current": copy_current,
    })


@mcp.tool()
def delete_scene(name: str) -> dict:
    """Delete a scene by name. Cannot delete the last scene.

    Args:
        name: Name of the scene to delete.
    """
    conn = get_blender_connection()
    return conn.send_command("delete_scene", {"name": Validator.validate_name(name)})


@mcp.tool()
def set_scene_property(property_name: str, value: str | int | float | bool) -> dict:
    """Set a scene-level property (e.g., frame_start, frame_end, fps, render_engine).

    Args:
        property_name: The property to set (e.g., 'frame_start', 'render_resolution_x').
        value: The value to set.
    """
    conn = get_blender_connection()
    return conn.send_command("set_scene_property", {
        "property_name": Validator.validate_name(property_name),
        "value": value,
    })


@mcp.tool()
def new_scene(name: str = "Scene") -> dict:
    """Create a fresh empty scene, replacing all current objects.

    Args:
        name: Name for the new clean scene.
    """
    conn = get_blender_connection()
    return conn.send_command("new_scene", {"name": Validator.validate_name(name)})


@mcp.tool()
def set_render_settings(
    engine: str = "CYCLES",
    resolution_x: int = 1920,
    resolution_y: int = 1080,
    resolution_percentage: int = 100,
    samples: int = 128,
    use_denoising: bool = True,
) -> dict:
    """Configure render settings in one call.

    Args:
        engine: Render engine (BLENDER_EEVEE, CYCLES, BLENDER_WORKBENCH).
        resolution_x: Output width in pixels.
        resolution_y: Output height in pixels.
        resolution_percentage: Resolution scale (1-100).
        samples: Number of render samples (for Cycles).
        use_denoising: Enable denoising.
    """
    conn = get_blender_connection()
    return conn.send_command("set_render_settings", {
        "engine": Validator.validate_enum(engine, "render_engine"),
        "resolution_x": Validator.validate_int(resolution_x, 64, 16384),
        "resolution_y": Validator.validate_int(resolution_y, 64, 16384),
        "resolution_percentage": Validator.validate_percentage(resolution_percentage),
        "samples": Validator.validate_int(samples, 1, 10000),
        "use_denoising": use_denoising,
    })
