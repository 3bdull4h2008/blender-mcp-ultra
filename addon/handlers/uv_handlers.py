"""UV mapping handlers."""

import bpy


def uv_smart_project(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=params.get("angle_limit", 66.0), island_margin=params.get("island_margin", 0.02))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "smart_projected"}


def uv_unwrap(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method=params.get("method", "ANGLE_BASED"))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "unwrapped"}


def uv_pack_islands(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.pack_islands(margin=params.get("margin", 0.001), rotate=params.get("rotate", True))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "packed"}


def uv_project_from_view(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.project_from_view()
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "projected_from_view"}


def uv_select_island(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.select_island()
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "island_selected"}


def get_uv_info(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{params['object_name']}' not found"}
    mesh = obj.data
    if not mesh.uv_layers:
        return {"has_uvs": False, "uv_layers": []}
    uv_layer = mesh.uv_layers.active
    uv_coords = [list(uv.data[i].uv) for i in range(len(uv_layer.data))]
    return {
        "has_uvs": True,
        "uv_layers": [l.name for l in mesh.uv_layers],
        "active_layer": uv_layer.name,
        "uv_count": len(uv_coords),
        "bounds": {
            "min_x": min(u[0] for u in uv_coords) if uv_coords else 0,
            "max_x": max(u[0] for u in uv_coords) if uv_coords else 1,
            "min_y": min(u[1] for u in uv_coords) if uv_coords else 0,
            "max_y": max(u[1] for u in uv_coords) if uv_coords else 1,
        },
    }


HANDLERS = {
    "uv_smart_project": uv_smart_project,
    "uv_unwrap": uv_unwrap,
    "uv_pack_islands": uv_pack_islands,
    "uv_project_from_view": uv_project_from_view,
    "uv_select_island": uv_select_island,
    "get_uv_info": get_uv_info,
}
