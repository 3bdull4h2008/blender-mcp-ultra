"""Collection management tools — organize objects into collections."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_collection(name: str, parent: str = "") -> dict:
    """Create a new collection.

    Args:
        name: Collection name.
        parent: Parent collection name (empty = root).
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if parent:
        params["parent"] = Validator.validate_name(parent)
    return conn.send_command("create_collection", params)


@mcp.tool()
def delete_collection(name: str, keep_objects: bool = True) -> dict:
    """Delete a collection.

    Args:
        name: Collection name.
        keep_objects: If True, move objects to the scene collection first.
    """
    conn = get_blender_connection()
    return conn.send_command("delete_collection", {
        "name": Validator.validate_name(name),
        "keep_objects": keep_objects,
    })


@mcp.tool()
def move_to_collection(object_name: str, collection_name: str) -> dict:
    """Move an object to a different collection.

    Args:
        object_name: Object to move.
        collection_name: Target collection.
    """
    conn = get_blender_connection()
    return conn.send_command("move_to_collection", {
        "object_name": Validator.validate_name(object_name),
        "collection_name": Validator.validate_name(collection_name),
    })


@mcp.tool()
def set_collection_visibility(collection_name: str, visible: bool = True) -> dict:
    """Toggle collection visibility in viewport.

    Args:
        collection_name: Collection name.
        visible: Show or hide.
    """
    conn = get_blender_connection()
    return conn.send_command("set_collection_visibility", {
        "collection_name": Validator.validate_name(collection_name),
        "visible": visible,
    })


@mcp.tool()
def list_collections() -> dict:
    """List all collections with their objects and hierarchy."""
    conn = get_blender_connection()
    return conn.send_command("list_collections")
