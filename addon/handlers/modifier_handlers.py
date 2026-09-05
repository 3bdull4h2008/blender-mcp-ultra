"""Modifier handlers — add, configure, apply, remove modifiers."""

import bpy


def add_modifier(params: dict) -> dict:
    obj_name = params["object_name"]
    mod_type = params["modifier_type"]
    mod_name = params.get("name", "")
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    mod = obj.modifiers.new(name=mod_name or mod_type, type=mod_type)
    # Apply extra settings
    for key, value in params.items():
        if key not in ("object_name", "modifier_type", "name") and hasattr(mod, key):
            try:
                setattr(mod, key, value)
            except (AttributeError, TypeError):
                pass
    return {"status": "added", "object": obj_name, "modifier": mod.name, "type": mod_type}


def configure_modifier(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mod = obj.modifiers.get(params["modifier_name"])
    if not mod:
        return {"error": f"Modifier '{params['modifier_name']}' not found"}
    for key, value in params.get("settings", {}).items():
        if hasattr(mod, key):
            try:
                setattr(mod, key, value)
            except (AttributeError, TypeError):
                pass
    return {"status": "configured", "modifier": mod.name}


def apply_modifier(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mod = obj.modifiers.get(params["modifier_name"])
    if not mod:
        return {"error": f"Modifier '{params['modifier_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return {"status": "applied", "modifier": mod.name}


def remove_modifier(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mod = obj.modifiers.get(params["modifier_name"])
    if not mod:
        return {"error": f"Modifier '{params['modifier_name']}' not found"}
    obj.modifiers.remove(mod)
    return {"status": "removed", "modifier": params["modifier_name"]}


def reorder_modifier(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mod = obj.modifiers.get(params["modifier_name"])
    if not mod:
        return {"error": f"Modifier '{params['modifier_name']}' not found"}
    new_idx = params.get("new_index", 0)
    # Blender doesn't have a direct reorder API, so we use a workaround
    bpy.context.view_layer.objects.active = obj
    for i in range(len(obj.modifiers)):
        if obj.modifiers[i].name == mod.name:
            while i > new_idx:
                bpy.ops.object.modifier_move_up(modifier=mod.name)
                i -= 1
            while i < new_idx:
                bpy.ops.object.modifier_move_down(modifier=mod.name)
                i += 1
            break
    return {"status": "reordered", "modifier": mod.name, "new_index": new_idx}


def boolean_operation(params: dict) -> dict:
    obj_name = params["object_name"]
    target_name = params["target_name"]
    operation = params.get("operation", "DIFFERENCE")

    obj = bpy.data.objects.get(obj_name)
    target = bpy.data.objects.get(target_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    if not target:
        return {"error": f"Target '{target_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
    mod.operation = operation
    mod.object = target
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(target, do_unlink=True)
    return {"status": "boolean_applied", "operation": operation, "object": obj_name}


def extrude_faces(params: dict) -> dict:
    obj_name = params["object_name"]
    distance = params.get("distance", 0.0)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, distance)})
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "extruded", "distance": distance}


def inset_faces(params: dict) -> dict:
    obj_name = params["object_name"]
    thickness = params.get("thickness", 0.1)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.inset_faces(thickness=thickness, use_boundary=params.get("use_boundary", True))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "insetted", "thickness": thickness}


def bevel_edges(params: dict) -> dict:
    obj_name = params["object_name"]
    width = params.get("width", 0.1)
    segments = params.get("segments", 1)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=width, segments=segments)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "beveled", "width": width, "segments": segments}


def loop_cut(params: dict) -> dict:
    obj_name = params["object_name"]
    cuts = params.get("number_cuts", 1)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.loopcut(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "loop_cut", "cuts": cuts}


def subdivide_mesh(params: dict) -> dict:
    obj_name = params["object_name"]
    cuts = params.get("cuts", 1)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "subdivided", "cuts": cuts}


def merge_vertices(params: dict) -> dict:
    obj_name = params["object_name"]
    distance = params.get("distance", 0.001)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.remove_doubles(threshold=distance)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "merged", "distance": distance}


def flip_normals(params: dict) -> dict:
    obj_name = params["object_name"]
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "normals_flipped"}


def recalculate_normals(params: dict) -> dict:
    obj_name = params["object_name"]
    outside = params.get("outside", True)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=not outside)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "normals_recalculated", "outside": outside}


HANDLERS = {
    "add_modifier": add_modifier,
    "configure_modifier": configure_modifier,
    "apply_modifier": apply_modifier,
    "remove_modifier": remove_modifier,
    "reorder_modifier": reorder_modifier,
    "boolean_operation": boolean_operation,
    "extrude_faces": extrude_faces,
    "inset_faces": inset_faces,
    "bevel_edges": bevel_edges,
    "loop_cut": loop_cut,
    "subdivide_mesh": subdivide_mesh,
    "merge_vertices": merge_vertices,
    "flip_normals": flip_normals,
    "recalculate_normals": recalculate_normals,
}
