"""Scene management handlers — bpy operations for scene inspection and configuration."""

import bpy


def get_scene_info(params: dict) -> dict:
    scene = bpy.context.scene
    objects = []
    for obj in scene.objects:
        objects.append({
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale),
            "visible": obj.visible_get(),
        })

    collections = []
    for col in bpy.data.collections:
        collections.append({
            "name": col.name,
            "object_count": len(col.objects),
            "parent": col.parent.name if col.parent else None,
        })

    return {
        "name": scene.name,
        "object_count": len(scene.objects),
        "objects": objects,
        "collections": collections,
        "frame_current": scene.frame_current,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "fps": scene.render.fps,
        "render_engine": scene.render.engine,
        "resolution_x": scene.render.resolution_x,
        "resolution_y": scene.render.resolution_y,
        "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
    }


def list_objects(params: dict) -> dict:
    object_type = params.get("object_type", "ALL")
    include_hidden = params.get("include_hidden", False)
    collection_name = params.get("collection")

    objects = []
    source = bpy.data.collections[collection_name].objects if collection_name else bpy.context.scene.objects

    for obj in source:
        if object_type != "ALL" and obj.type != object_type:
            continue
        if not include_hidden and not obj.visible_get():
            continue
        objects.append({
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale),
            "visible": obj.visible_get(),
        })

    return {"objects": objects, "count": len(objects)}


def get_object_info(params: dict) -> dict:
    name = params["object_name"]
    obj = bpy.data.objects.get(name)
    if not obj:
        return {"error": f"Object '{name}' not found"}

    info = {
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
        "dimensions": list(obj.dimensions),
        "visible": obj.visible_get(),
        "selectable": obj.select_get(),
        "materials": [m.name if m else None for m in obj.material_slots],
        "modifiers": [{"name": m.name, "type": m.type} for m in obj.modifiers],
        "constraints": [{"name": c.name, "type": c.type} for c in obj.constraints],
        "vertex_groups": [vg.name for vg in obj.vertex_groups] if obj.type == 'MESH' else [],
        "shape_keys": [sk.name for sk in obj.data.shape_keys.key_blocks] if obj.data and hasattr(obj.data, 'shape_keys') and obj.data.shape_keys else [],
    }

    if obj.type == 'MESH':
        mesh = obj.data
        info["mesh_stats"] = {
            "vertex_count": len(mesh.vertices),
            "edge_count": len(mesh.edges),
            "face_count": len(mesh.polygons),
            "triangle_count": sum(1 for p in mesh.polygons if len(p.vertices) == 3),
            "ngon_count": sum(1 for p in mesh.polygons if len(p.vertices) > 4),
        }

    bbox = obj.bound_box
    info["bounding_box"] = {
        "min": [min(bbox[i][j] for i in range(8)) for j in range(3)],
        "max": [max(bbox[i][j] for i in range(8)) for j in range(3)],
    }

    return info


def create_scene(params: dict) -> dict:
    name = params.get("name", "Scene")
    copy = params.get("copy_current", False)
    bpy.ops.scene.new(type='COPY' if copy else 'EMPTY')
    bpy.context.scene.name = name
    return {"status": "created", "name": name}


def delete_scene(params: dict) -> dict:
    name = params["name"]
    scene = bpy.data.scenes.get(name)
    if not scene:
        return {"error": f"Scene '{name}' not found"}
    if len(bpy.data.scenes) <= 1:
        return {"error": "Cannot delete the last scene"}
    bpy.data.scenes.remove(scene)
    return {"status": "deleted", "name": name}


def set_scene_property(params: dict) -> dict:
    prop = params["property_name"]
    value = params["value"]
    scene = bpy.context.scene
    if hasattr(scene, prop):
        setattr(scene, prop, value)
        return {"status": "set", "property": prop, "value": value}
    return {"error": f"Property '{prop}' not found on scene"}


def new_scene(params: dict) -> dict:
    name = params.get("name", "Scene")
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.context.scene.name = name
    return {"status": "created", "name": name}


def set_render_settings(params: dict) -> dict:
    scene = bpy.context.scene
    if "engine" in params:
        scene.render.engine = params["engine"]
    if "resolution_x" in params:
        scene.render.resolution_x = params["resolution_x"]
    if "resolution_y" in params:
        scene.render.resolution_y = params["resolution_y"]
    if "resolution_percentage" in params:
        scene.render.resolution_percentage = int(params["resolution_percentage"])
    if "samples" in params:
        engine = scene.render.engine
        if engine == 'CYCLES':
            scene.cycles.samples = params["samples"]
    if "use_denoising" in params:
        scene.cycles.use_denoising = params["use_denoising"]
    return {"status": "render_settings_updated"}


HANDLERS = {
    "get_scene_info": get_scene_info,
    "list_objects": list_objects,
    "get_object_info": get_object_info,
    "create_scene": create_scene,
    "delete_scene": delete_scene,
    "set_scene_property": set_scene_property,
    "new_scene": new_scene,
    "set_render_settings": set_render_settings,
}
