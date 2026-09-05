"""Animation tools — keyframes, timeline, NLA, constraints."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def set_keyframe(
    object_name: str,
    frame: int = None,
    location: bool = True,
    rotation: bool = True,
    scale: bool = False,
    property_name: str = "",
) -> dict:
    """Insert keyframes for an object.

    Args:
        object_name: Target object.
        frame: Frame number (None = current frame).
        location: Keyframe location.
        rotation: Keyframe rotation.
        scale: Keyframe scale.
        property_name: Optional custom property to keyframe.
    """
    conn = get_blender_connection()
    params = {
        "object_name": Validator.validate_name(object_name),
        "location": location,
        "rotation": rotation,
        "scale": scale,
    }
    if frame is not None:
        params["frame"] = Validator.validate_int(frame, 0, 100000)
    if property_name:
        params["property_name"] = property_name
    return conn.send_command("set_keyframe", params)


@mcp.tool()
def delete_keyframe(
    object_name: str,
    frame: int = None,
) -> dict:
    """Delete keyframes at a specific frame or all keyframes.

    Args:
        object_name: Target object.
        frame: Frame to delete (None = all keyframes).
    """
    conn = get_blender_connection()
    params = {"object_name": Validator.validate_name(object_name)}
    if frame is not None:
        params["frame"] = Validator.validate_int(frame, 0, 100000)
    return conn.send_command("delete_keyframe", params)


@mcp.tool()
def set_interpolation(
    object_name: str,
    interpolation: str = "BEZIER",
    easing: str = "AUTO",
) -> dict:
    """Set keyframe interpolation mode for an object's animation.

    Args:
        object_name: Target object.
        interpolation: CONSTANT, LINEAR, BEZIER, etc.
        easing: AUTO, EASE_IN, EASE_OUT, EASE_IN_OUT.
    """
    conn = get_blender_connection()
    return conn.send_command("set_interpolation", {
        "object_name": Validator.validate_name(object_name),
        "interpolation": interpolation.upper(),
        "easing": easing.upper(),
    })


@mcp.tool()
def set_animation_range(
    start_frame: int = 1,
    end_frame: int = 250,
    frame_step: int = 1,
) -> dict:
    """Set the animation playback range.

    Args:
        start_frame: Start frame.
        end_frame: End frame.
        frame_step: Step between frames.
    """
    conn = get_blender_connection()
    return conn.send_command("set_animation_range", {
        "start_frame": Validator.validate_int(start_frame, 0, 1000000),
        "end_frame": Validator.validate_int(end_frame, 1, 1000000),
        "frame_step": Validator.validate_int(frame_step, 1, 100),
    })


@mcp.tool()
def set_fps(fps: int = 24) -> dict:
    """Set the scene frame rate.

    Args:
        fps: Frames per second (1-1000).
    """
    conn = get_blender_connection()
    return conn.send_command("set_fps", {"fps": Validator.validate_int(fps, 1, 1000)})


@mcp.tool()
def go_to_frame(frame: int = 1) -> dict:
    """Jump to a specific frame in the timeline.

    Args:
        frame: Frame number.
    """
    conn = get_blender_connection()
    return conn.send_command("go_to_frame", {"frame": Validator.validate_int(frame, 0, 1000000)})


@mcp.tool()
def create_walk_cycle(
    object_name: str,
    frames_per_cycle: int = 32,
    amplitude: float = 0.2,
) -> dict:
    """Create a simple walk/bounce cycle animation.

    Args:
        object_name: Target object.
        frames_per_cycle: Frames for one full cycle.
        amplitude: Bounce height.
    """
    conn = get_blender_connection()
    return conn.send_command("create_walk_cycle", {
        "object_name": Validator.validate_name(object_name),
        "frames_per_cycle": Validator.validate_int(frames_per_cycle, 4, 1000),
        "amplitude": Validator.validate_float(amplitude, 0.01, 100),
    })


@mcp.tool()
def setup_subdivision_animation(
    object_name: str,
    modifier_name: str = "Subdivision",
    start_level: int = 0,
    end_level: int = 3,
    start_frame: int = 1,
    end_frame: int = 60,
) -> dict:
    """Animate a subdivision surface modifier's viewport levels.

    Args:
        object_name: Target object.
        modifier_name: Name of the subdivision modifier.
        start_level: Starting subdivision level.
        end_level: Ending subdivision level.
        start_frame: Start frame.
        end_frame: End frame.
    """
    conn = get_blender_connection()
    return conn.send_command("setup_subdivision_animation", {
        "object_name": Validator.validate_name(object_name),
        "modifier_name": Validator.validate_name(modifier_name),
        "start_level": Validator.validate_int(start_level, 0, 6),
        "end_level": Validator.validate_int(end_level, 0, 6),
        "start_frame": Validator.validate_int(start_frame, 0, 1000000),
        "end_frame": Validator.validate_int(end_frame, 1, 1000000),
    })
