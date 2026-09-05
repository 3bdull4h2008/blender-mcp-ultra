"""File import/export tools — FBX, OBJ, glTF, USD, Alembic."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def import_file(
    filepath: str,
    file_type: str = "",
    **kwargs,
) -> dict:
    """Import a 3D model file.

    Args:
        filepath: Path to the file to import.
        file_type: FBX, OBJ, GLTF, GLB, STL, USD, PLY, ABC, etc. (auto-detected from extension if empty).
    """
    conn = get_blender_connection()
    params = {"filepath": Validator.validate_path(filepath)}
    if file_type:
        params["file_type"] = file_type.upper()
    params.update(kwargs)
    return conn.send_command("import_file", params)


@mcp.tool()
def export_file(
    filepath: str,
    file_type: str = "",
    selected_only: bool = False,
    **kwargs,
) -> dict:
    """Export objects to a 3D model file.

    Args:
        filepath: Output file path.
        file_type: FBX, OBJ, GLTF, GLB, STL, USD, PLY, ABC, etc.
        selected_only: Only export selected objects.
    """
    conn = get_blender_connection()
    params = {
        "filepath": Validator.validate_path(filepath),
        "selected_only": selected_only,
    }
    if file_type:
        params["file_type"] = file_type.upper()
    params.update(kwargs)
    return conn.send_command("export_file", params)


@mcp.tool()
def export_fbx(
    filepath: str,
    selected_only: bool = False,
    apply_scale: bool = True,
    mesh_smooth_type: str = "OFF",
    path_mode: str = "AUTO",
) -> dict:
    """Export to FBX format with common settings.

    Args:
        filepath: Output path.
        selected_only: Only export selected.
        apply_scale: Apply scale transforms.
        mesh_smooth_type: OFF, FACE, or EDGE.
        path_mode: AUTO, ABSOLUTE, RELATIVE, MATCH, STRIP, COPY.
    """
    conn = get_blender_connection()
    return conn.send_command("export_fbx", {
        "filepath": Validator.validate_path(filepath),
        "selected_only": selected_only,
        "apply_scale": apply_scale,
        "mesh_smooth_type": mesh_smooth_type.upper(),
        "path_mode": path_mode.upper(),
    })


@mcp.tool()
def export_glb(
    filepath: str,
    selected_only: bool = False,
    export_materials: bool = True,
) -> dict:
    """Export to glTF binary (GLB) format.

    Args:
        filepath: Output path.
        selected_only: Only export selected.
        export_materials: Include materials.
    """
    conn = get_blender_connection()
    return conn.send_command("export_glb", {
        "filepath": Validator.validate_path(filepath),
        "selected_only": selected_only,
        "export_materials": export_materials,
    })


@mcp.tool()
def export_obj(
    filepath: str,
    selected_only: bool = False,
    export_materials: bool = True,
) -> dict:
    """Export to OBJ format.

    Args:
        filepath: Output path.
        selected_only: Only export selected.
        export_materials: Include MTL file.
    """
    conn = get_blender_connection()
    return conn.send_command("export_obj", {
        "filepath": Validator.validate_path(filepath),
        "selected_only": selected_only,
        "export_materials": export_materials,
    })
