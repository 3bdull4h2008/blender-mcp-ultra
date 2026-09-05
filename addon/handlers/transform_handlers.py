"""Transform handlers — move, rotate, scale, align objects."""

import bpy
import math
import mathutils


def set_object_transform(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    space = params.get("space", "WORLD")
    if "location" in params:
        if space == "LOCAL" and obj.parent:
            obj.matrix_parent_inverse = obj.parent.matrix_world.inverted()
        obj.location = params["location"]
    if "rotation" in params:
        obj.rotation_euler = params["rotation"]
    if "scale" in params:
        obj.scale = params["scale"]
    return {"status": "transform_set", "name": name, "space": space}


def move_object(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    dx, dy, dz = params.get("x", 0), params.get("y", 0), params.get("z", 0)
    space = params.get("space", "WORLD")
    if space == "LOCAL":
        local_offset = obj.matrix_world.to_3x3() @ mathutils.Vector((dx, dy, dz))
        obj.location += local_offset
    else:
        obj.location.x += dx
        obj.location.y += dy
        obj.location.z += dz
    return {"status": "moved", "name": name, "delta": [dx, dy, dz], "space": space}


def rotate_object(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    rx, ry, rz = params.get("x", 0), params.get("y", 0), params.get("z", 0)
    space = params.get("space", "WORLD")
    if space == "LOCAL":
        local_rot = mathutils.Euler((rx, ry, rz))
        obj.rotation_euler.rotate(local_rot)
    else:
        obj.rotation_euler.x += rx
        obj.rotation_euler.y += ry
        obj.rotation_euler.z += rz
    return {"status": "rotated", "name": name, "delta": [rx, ry, rz], "space": space}


def scale_object(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    sx, sy, sz = params.get("x", 1), params.get("y", 1), params.get("z", 1)
    obj.scale.x *= sx
    obj.scale.y *= sy
    obj.scale.z *= sz
    return {"status": "scaled", "name": name, "factors": [sx, sy, sz]}


def apply_transform(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    loc = params.get("location", True)
    rot = params.get("rotation", True)
    sca = params.get("scale", True)
    bpy.ops.object.transform_apply(location=loc, rotation=rot, scale=sca)
    return {"status": "transform_applied", "name": name}


def get_local_transforms(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    if obj.parent:
        mat = obj.parent.matrix_world.inverted() @ obj.matrix_world
        loc, rot, sca = mat.decompose()
        return {
            "name": name,
            "location": list(loc),
            "rotation": list(rot),
            "scale": list(sca),
        }
    return {
        "name": name,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
    }


def align_object(params: dict) -> dict:
    name = params["name"]
    target_name = params["target"]
    obj = bpy.data.objects.get(name)
    target = bpy.data.objects.get(target_name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    if not target:
        return {"error": f"Target '{target_name}' not found"}
    if params.get("align_location", True):
        obj.location = target.location.copy()
    if params.get("align_rotation", False):
        obj.rotation_euler = target.rotation_euler.copy()
    if params.get("align_scale", False):
        obj.scale = target.scale.copy()
    return {"status": "aligned", "name": name, "target": target_name}


def snap_to_cursor(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    if "cursor_location" in params:
        bpy.context.scene.cursor.location = params["cursor_location"]
    obj.location = bpy.context.scene.cursor.location.copy()
    return {"status": "snapped", "name": name}


HANDLERS = {
    "set_object_transform": set_object_transform,
    "move_object": move_object,
    "rotate_object": rotate_object,
    "scale_object": scale_object,
    "apply_transform": apply_transform,
    "get_local_transforms": get_local_transforms,
    "align_object": align_object,
    "snap_to_cursor": snap_to_cursor,
}
