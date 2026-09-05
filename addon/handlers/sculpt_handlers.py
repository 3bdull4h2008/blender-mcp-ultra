"""Sculpt handlers — brush configuration, sculpt mode operations."""

import bpy


def configure_sculpt_brush(params: dict) -> dict:
    brush_name = params.get("brush_name", "Draw")
    size = params.get("size", 50.0)
    strength = params.get("strength", 0.5)

    brush = bpy.data.brushes.get(brush_name)
    if not brush:
        return {"error": f"Brush '{brush_name}' not found"}
    brush.size = int(size)
    brush.strength = strength
    return {"status": "brush_configured", "name": brush.name, "size": brush.size, "strength": brush.strength}


def enter_sculpt_mode(params: dict) -> dict:
    obj_name = params.get("object_name", "")
    if obj_name:
        obj = bpy.data.objects.get(obj_name)
        if obj:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
    bpy.ops.object.mode_set(mode='SCULPT')
    return {"status": "sculpt_mode_entered"}


def exit_sculpt_mode(params: dict) -> dict:
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "sculpt_mode_exited"}


def set_sculpt_symmetry(params: dict) -> dict:
    obj = bpy.context.active_object
    if not obj:
        return {"error": "No active object"}
    props = obj.data.sculpt
    props.use_symmetry_x = params.get("axis_x", True)
    props.use_symmetry_y = params.get("axis_y", False)
    props.use_symmetry_z = params.get("axis_z", False)
    return {"status": "symmetry_set"}


def configure_dyntopo(params: dict) -> dict:
    obj = bpy.context.active_object
    if not obj or obj.mode != 'SCULPT':
        return {"error": "Must be in sculpt mode"}
    props = obj.data.sculpt
    props.use_dyntopo = params.get("enabled", True)
    if params.get("enabled"):
        props.detail_type_method = params.get("resolution", "RELATIVE").lower()
        props.constant_detail_resolution = params.get("detail_size", 12.0)
    return {"status": "dyntopo_configured"}


def remesh_sculpt(params: dict) -> dict:
    mode = params.get("mode", "VOXEL")
    voxel_size = params.get("voxel_size", 0.1)
    obj = bpy.context.active_object
    if not obj:
        return {"error": "No active object"}
    bpy.ops.object.mode_set(mode='OBJECT')
    if mode == "VOXEL":
        bpy.ops.object.voxel_remesh(voxel_size=voxel_size)
    else:
        bpy.ops.object.quadriflow_remesh()
    return {"status": "remeshed", "mode": mode}


HANDLERS = {
    "configure_sculpt_brush": configure_sculpt_brush,
    "enter_sculpt_mode": enter_sculpt_mode,
    "exit_sculpt_mode": exit_sculpt_mode,
    "set_sculpt_symmetry": set_sculpt_symmetry,
    "configure_dyntopo": configure_dyntopo,
    "remesh_sculpt": remesh_sculpt,
}
