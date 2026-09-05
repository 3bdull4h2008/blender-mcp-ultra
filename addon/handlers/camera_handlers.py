"""Camera handlers — create, configure, animate cameras."""

import bpy
import math


def create_camera(params: dict) -> dict:
    name = params.get("name", "Camera")
    location = params.get("location", (0, -5, 2))
    rotation = params.get("rotation", (math.radians(75), 0, 0))
    lens = params.get("lens", 50.0)

    bpy.ops.object.camera_add(location=location, rotation=rotation)
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    cam.data.sensor_width = params.get("sensor_width", 36.0)
    cam.data.clip_start = params.get("clip_start", 0.1)
    cam.data.clip_end = params.get("clip_end", 1000.0)
    bpy.context.scene.camera = cam
    return {"status": "created", "name": cam.name, "lens": lens}


def configure_camera(params: dict) -> dict:
    name = params["name"]
    cam_obj = bpy.data.objects.get(name)
    if not cam_obj or cam_obj.type != 'CAMERA':
        return {"error": f"Camera '{name}' not found"}
    data = cam_obj.data
    if "lens" in params:
        data.lens = params["lens"]
    if "depth_of_field" in params:
        data.dof.use_dof = params["depth_of_field"]
    if "fstop" in params:
        data.dof.aperture_fstop = params["fstop"]
    if "focus_distance" in params:
        data.dof.focus_distance = params["focus_distance"]
    if "clip_start" in params:
        data.clip_start = params["clip_start"]
    if "clip_end" in params:
        data.clip_end = params["clip_end"]
    return {"status": "configured", "name": name}


def set_camera_to_view(params: dict) -> dict:
    cam_name = params.get("name", "")
    target_name = params.get("target_name", "")
    distance = params.get("distance", 5.0)

    cam = bpy.data.objects.get(cam_name) if cam_name else bpy.context.scene.camera
    if not cam:
        return {"error": "No camera found"}

    if target_name:
        target = bpy.data.objects.get(target_name)
        if target:
            cam.location = target.location.copy()
            cam.location.y -= distance
            cam.location.z += distance * 0.4
            direction = target.location - cam.location
            rot_quat = direction.to_track_quat('-Z', 'Y')
            cam.rotation_euler = rot_quat.to_euler()
    return {"status": "camera_positioned", "name": cam.name}


def setup_camera_track_to(params: dict) -> dict:
    cam_name = params["camera_name"]
    target_name = params["target_name"]
    cam = bpy.data.objects.get(cam_name)
    target = bpy.data.objects.get(target_name)
    if not cam:
        return {"error": f"Camera '{cam_name}' not found"}
    if not target:
        return {"error": f"Target '{target_name}' not found"}

    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    return {"status": "track_to_set", "camera": cam_name, "target": target_name}


def setup_turntable_camera(params: dict) -> dict:
    name = params.get("name", "TurntableCamera")
    target = params.get("target", [0, 0, 0])
    distance = params.get("distance", 5.0)
    height = params.get("height", 2.0)
    frames = params.get("frames", 120)

    bpy.ops.object.camera_add(location=(distance, 0, height))
    cam = bpy.context.active_object
    cam.name = name

    # Add Track To constraint
    empty = bpy.ops.object.empty_add(type='PLAIN_AXES', location=target)
    empty_obj = bpy.context.active_object
    empty_obj.name = "Turntable_Target"

    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = empty_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    # Animate orbit
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames
    for f in range(1, frames + 1):
        angle = (f / frames) * 2 * math.pi
        cam.location.x = target[0] + distance * math.cos(angle)
        cam.location.y = target[1] + distance * math.sin(angle)
        cam.location.z = height
        cam.keyframe_insert(data_path="location", frame=f)

    return {"status": "turntable_created", "camera": name, "frames": frames}


HANDLERS = {
    "create_camera": create_camera,
    "configure_camera": configure_camera,
    "set_camera_to_view": set_camera_to_view,
    "setup_camera_track_to": setup_camera_track_to,
    "setup_turntable_camera": setup_turntable_camera,
}
