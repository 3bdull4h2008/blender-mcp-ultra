"""Object management handlers — create, delete, duplicate, organize objects."""

import bpy


def create_object(params: dict) -> dict:
    obj_type = params.get("object_type", "MESH")
    name = params.get("name", "Object")
    location = params.get("location", (0, 0, 0))
    rotation = params.get("rotation", (0, 0, 0))
    scale = params.get("scale", (1, 1, 1))

    if obj_type == "MESH":
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    elif obj_type == "LIGHT":
        bpy.ops.object.light_add(type='POINT', location=location)
    elif obj_type == "CAMERA":
        bpy.ops.object.camera_add(location=location, rotation=rotation)
    elif obj_type == "EMPTY":
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    elif obj_type == "CURVE":
        bpy.ops.curve.primitive_bezier_circle_add(location=location)
    elif obj_type == "ARMATURE":
        bpy.ops.object.armature_add(location=location)
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)

    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    obj.scale = scale
    return {"status": "created", "name": obj.name, "type": obj.type}


def delete_object(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    bpy.data.objects.remove(obj, do_unlink=True)
    return {"status": "deleted", "name": name}


def duplicate_object(params: dict) -> dict:
    name = params["name"]
    new_name = params.get("new_name", "")
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()
    bpy.context.scene.objects.link(new_obj)
    if new_name:
        new_obj.name = new_name
    return {"status": "duplicated", "name": new_obj.name}


def rename_object(params: dict) -> dict:
    name = params["name"]
    new_name = params["new_name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    obj.name = new_name
    return {"status": "renamed", "old_name": name, "new_name": new_name}


def select_objects(params: dict) -> dict:
    names = params["names"]
    replace = params.get("replace", True)
    if replace:
        bpy.ops.object.select_all(action='DESELECT')
    for n in names:
        obj = bpy.data.objects.get(n)
        if obj:
            obj.select_set(True)
    return {"status": "selected", "names": names}


def set_object_visibility(params: dict) -> dict:
    name = params["name"]
    visible = params.get("visible", True)
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    obj.hide_viewport = not visible
    obj.hide_render = params.get("hide_render", False)
    return {"status": "visibility_set", "name": name, "visible": visible}


def parent_objects(params: dict) -> dict:
    child = bpy.data.objects.get(params["child"])
    parent = bpy.data.objects.get(params["parent"])
    if not child:
        return {"error": f"Child '{params['child']}' not found"}
    if not parent:
        return {"error": f"Parent '{params['parent']}' not found"}
    keep = params.get("keep_transform", True)
    child.parent = parent
    if not keep:
        child.matrix_parent_inverse = parent.matrix_world.inverted()
    return {"status": "parented", "child": child.name, "parent": parent.name}


def join_objects(params: dict) -> dict:
    names = params["names"]
    objs = [bpy.data.objects.get(n) for n in names]
    objs = [o for o in objs if o is not None]
    if len(objs) < 2:
        return {"error": "Need at least 2 objects to join"}
    bpy.context.view_layer.objects.active = objs[0]
    for o in objs:
        o.select_set(True)
    bpy.ops.object.join()
    return {"status": "joined", "result": objs[0].name, "count": len(objs)}


def set_origin(params: dict) -> dict:
    name = params["name"]
    origin_type = params.get("origin_type", "GEOMETRY")
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    type_map = {
        "GEOMETRY": 'ORIGIN_GEOMETRY',
        "CURSOR": 'ORIGIN_CURSOR',
        "CENTER_OF_MASS": 'ORIGIN_CENTER_OF_MASS',
        "CENTER_OF_VOLUME": 'ORIGIN_CENTER_OF_VOLUME',
    }
    bpy.ops.object.origin_set(type=type_map.get(origin_type, 'ORIGIN_GEOMETRY'))
    return {"status": "origin_set", "name": name, "type": origin_type}


def convert_object(params: dict) -> dict:
    name = params["name"]
    target = params.get("target_type", "MESH")
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if target == "MESH":
        bpy.ops.object.convert(target='MESH')
    return {"status": "converted", "name": name, "target": target}


def shade_object(params: dict) -> dict:
    name = params["name"]
    shading = params.get("shading", "SMOOTH")
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if shading == "SMOOTH":
        bpy.ops.object.shade_smooth()
    else:
        bpy.ops.object.shade_flat()
    return {"status": "shaded", "name": name, "shading": shading}


HANDLERS = {
    "create_object": create_object,
    "delete_object": delete_object,
    "duplicate_object": duplicate_object,
    "rename_object": rename_object,
    "select_objects": select_objects,
    "set_object_visibility": set_object_visibility,
    "parent_objects": parent_objects,
    "join_objects": join_objects,
    "set_origin": set_origin,
    "convert_object": convert_object,
    "shade_object": shade_object,
}
