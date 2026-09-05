"""Animation handlers — keyframes, timeline, interpolation."""

import bpy
import math


def set_keyframe(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    frame = params.get("frame")
    if frame is not None:
        bpy.context.scene.frame_set(frame)
    if params.get("location", True):
        obj.keyframe_insert(data_path="location")
    if params.get("rotation", True):
        obj.keyframe_insert(data_path="rotation_euler")
    if params.get("scale", False):
        obj.keyframe_insert(data_path="scale")
    prop = params.get("property_name")
    if prop:
        obj.keyframe_insert(data_path=f'["{prop}"]')
    return {"status": "keyframe_set", "object": obj.name, "frame": frame or bpy.context.scene.frame_current}


def delete_keyframe(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    frame = params.get("frame")
    if frame and obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in list(fc.keyframe_points):
                if kp.co[0] == frame:
                    fc.keyframe_points.remove(kp)
    elif not frame:
        if obj.animation_data:
            obj.animation_data_clear()
    return {"status": "keyframes_deleted"}


def set_interpolation(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    interp = params.get("interpolation", "BEZIER")
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = interp
    return {"status": "interpolation_set", "mode": interp}


def set_animation_range(params: dict) -> dict:
    scene = bpy.context.scene
    scene.frame_start = params.get("start_frame", 1)
    scene.frame_end = params.get("end_frame", 250)
    scene.frame_step = params.get("frame_step", 1)
    return {"status": "range_set", "start": scene.frame_start, "end": scene.frame_end}


def set_fps(params: dict) -> dict:
    bpy.context.scene.render.fps = params.get("fps", 24)
    return {"status": "fps_set", "fps": bpy.context.scene.render.fps}


def go_to_frame(params: dict) -> dict:
    frame = params.get("frame", 1)
    bpy.context.scene.frame_set(frame)
    return {"status": "frame_set", "frame": frame}


def create_walk_cycle(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    frames_per_cycle = params.get("frames_per_cycle", 32)
    amplitude = params.get("amplitude", 0.2)
    base_y = obj.location.y
    base_z = obj.location.z
    for i in range(frames_per_cycle):
        f = i + 1
        t = i / frames_per_cycle * 2 * math.pi
        obj.location.y = base_y + amplitude * math.sin(t)
        obj.location.z = base_z + amplitude * 0.5 * abs(math.sin(t * 2))
        obj.keyframe_insert(data_path="location", frame=f)
    return {"status": "walk_cycle_created", "frames": frames_per_cycle}


def setup_subdivision_animation(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mod_name = params.get("modifier_name", "Subdivision")
    mod = obj.modifiers.get(mod_name)
    if not mod:
        return {"error": f"Modifier '{mod_name}' not found"}
    start = params.get("start_frame", 1)
    end = params.get("end_frame", 60)
    start_level = params.get("start_level", 0)
    end_level = params.get("end_level", 3)
    mid = (start + end) // 2
    mid_level = (start_level + end_level) // 2
    mod.levels = start_level
    mod.keyframe_insert(data_path="levels", frame=start)
    mod.levels = mid_level
    mod.keyframe_insert(data_path="levels", frame=mid)
    mod.levels = end_level
    mod.keyframe_insert(data_path="levels", frame=end)
    return {"status": "subdivision_animated"}


HANDLERS = {
    "set_keyframe": set_keyframe,
    "delete_keyframe": delete_keyframe,
    "set_interpolation": set_interpolation,
    "set_animation_range": set_animation_range,
    "set_fps": set_fps,
    "go_to_frame": go_to_frame,
    "create_walk_cycle": create_walk_cycle,
    "setup_subdivision_animation": setup_subdivision_animation,
}
