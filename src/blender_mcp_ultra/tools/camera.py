"""Camera tools — create, configure, animate cameras."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_camera(
    name: str = "Camera",
    location: list[float] = None,
    rotation: list[float] = None,
    lens: float = 50.0,
    sensor_width: float = 36.0,
    clip_start: float = 0.1,
    clip_end: float = 1000.0,
) -> dict:
    """Create a camera with optical settings.

    Args:
        name: Camera name.
        location: [x, y, z] position.
        rotation: [x, y, z] Euler rotation.
        lens: Focal length in mm.
        sensor_width: Sensor width in mm.
        clip_start: Near clipping distance.
        clip_end: Far clipping distance.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "lens": Validator.validate_float(lens, 1, 10000),
        "sensor_width": Validator.validate_float(sensor_width, 1, 1000),
        "clip_start": Validator.validate_float(clip_start, 0.001, 1000),
        "clip_end": Validator.validate_float(clip_end, 1, 1000000),
    }
    if location:
        params["location"] = Validator.validate_vector(location)
    if rotation:
        params["rotation"] = Validator.validate_vector(rotation)
    return conn.send_command("create_camera", params)


@mcp.tool()
def configure_camera(
    name: str,
    lens: float = None,
    depth_of_field: bool = None,
    fstop: float = None,
    focus_distance: float = None,
    clip_start: float = None,
    clip_end: float = None,
) -> dict:
    """Configure camera optical properties.

    Args:
        name: Camera object name.
        lens: Focal length in mm.
        depth_of_field: Enable depth of field.
        fstop: Aperture f-stop.
        focus_distance: Focus distance.
        clip_start: Near clip.
        clip_end: Far clip.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if lens is not None:
        params["lens"] = Validator.validate_float(lens, 1, 10000)
    if depth_of_field is not None:
        params["depth_of_field"] = depth_of_field
    if fstop is not None:
        params["fstop"] = Validator.validate_float(fstop, 0.01, 256)
    if focus_distance is not None:
        params["focus_distance"] = Validator.validate_float(focus_distance, 0.001, 100000)
    if clip_start is not None:
        params["clip_start"] = Validator.validate_float(clip_start, 0.001, 1000)
    if clip_end is not None:
        params["clip_end"] = Validator.validate_float(clip_end, 1, 1000000)
    return conn.send_command("configure_camera", params)


@mcp.tool()
def set_camera_to_view(
    name: str = "",
    target_name: str = "",
    distance: float = 5.0,
) -> dict:
    """Position camera to frame the current viewport or a specific object.

    Args:
        name: Camera name (empty = active camera).
        target_name: Object to frame (empty = all visible).
        distance: Distance from target.
    """
    conn = get_blender_connection()
    params = {"distance": Validator.validate_float(distance, 0.1, 10000)}
    if name:
        params["name"] = Validator.validate_name(name)
    if target_name:
        params["target_name"] = Validator.validate_name(target_name)
    return conn.send_command("set_camera_to_view", params)


@mcp.tool()
def setup_camera_track_to(camera_name: str, target_name: str) -> dict:
    """Make a camera always point at a target object (Track To constraint).

    Args:
        camera_name: Camera to constrain.
        target_name: Object to track.
    """
    conn = get_blender_connection()
    return conn.send_command("setup_camera_track_to", {
        "camera_name": Validator.validate_name(camera_name),
        "target_name": Validator.validate_name(target_name),
    })


@mcp.tool()
def setup_turntable_camera(
    name: str = "TurntableCamera",
    target: list[float] = None,
    distance: float = 5.0,
    height: float = 2.0,
    frames: int = 120,
) -> dict:
    """Set up a turntable camera animation (360-degree orbit).

    Args:
        name: Camera name.
        target: [x, y, z] point to orbit around.
        distance: Orbit radius.
        height: Camera height.
        frames: Number of frames for one revolution.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "distance": Validator.validate_float(distance, 0.1, 1000),
        "height": Validator.validate_float(height),
        "frames": Validator.validate_int(frames, 10, 10000),
    }
    if target:
        params["target"] = Validator.validate_vector(target)
    return conn.send_command("setup_turntable_camera", params)
