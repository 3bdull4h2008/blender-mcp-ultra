"""Collection handlers."""

import bpy


def create_collection(params: dict) -> dict:
    name = params["name"]
    parent_name = params.get("parent", "")
    col = bpy.data.collections.new(name)
    if parent_name:
        parent = bpy.data.collections.get(parent_name)
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    return {"status": "created", "name": col.name}


def delete_collection(params: dict) -> dict:
    name = params["name"]
    col = bpy.data.collections.get(name)
    if not col:
        return {"error": f"Collection '{name}' not found"}
    if params.get("keep_objects", True):
        scene_col = bpy.context.scene.collection
        for obj in list(col.objects):
            scene_col.objects.link(obj)
    bpy.data.collections.remove(col)
    return {"status": "deleted", "name": name}


def move_to_collection(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    col = bpy.data.collections.get(params["collection_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    if not col:
        return {"error": f"Collection '{params['collection_name']}' not found"}
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)
    return {"status": "moved", "object": obj.name, "collection": col.name}


def set_collection_visibility(params: dict) -> dict:
    col = bpy.data.collections.get(params["collection_name"])
    if not col:
        return {"error": f"Collection '{params['collection_name']}' not found"}
    col.hide_viewport = not params.get("visible", True)
    return {"status": "visibility_set"}


def list_collections(params: dict) -> dict:
    collections = []
    for col in bpy.data.collections:
        collections.append({
            "name": col.name,
            "object_count": len(col.objects),
            "parent": col.parent.name if col.parent else None,
            "children": [c.name for c in col.children],
        })
    return {"collections": collections, "count": len(collections)}


HANDLERS = {
    "create_collection": create_collection,
    "delete_collection": delete_collection,
    "move_to_collection": move_to_collection,
    "set_collection_visibility": set_collection_visibility,
    "list_collections": list_collections,
}
