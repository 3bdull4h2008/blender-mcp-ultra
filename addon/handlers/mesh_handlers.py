"""Mesh editing handlers — vertex, edge, face operations."""

import bpy
import bmesh


def edit_mesh_vertices(params: dict) -> dict:
    obj_name = params["object_name"]
    action = params.get("action", "move")
    vertices = params.get("vertices")
    offset = params.get("offset", [0, 0, 0])

    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    if action == "move" and vertices:
        for vi in vertices:
            if vi < len(bm.verts):
                bm.verts[vi].co.x += offset[0]
                bm.verts[vi].co.y += offset[1]
                bm.verts[vi].co.z += offset[2]
    elif action == "delete" and vertices:
        verts_to_delete = [bm.verts[vi] for vi in vertices if vi < len(bm.verts)]
        bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
    elif action == "smooth":
        bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, iterations=1)

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": f"vertices_{action}", "count": len(vertices) if vertices else 0}


def edit_mesh_edges(params: dict) -> dict:
    obj_name = params["object_name"]
    action = params.get("action", "select")

    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    if action == "mark_seam":
        bpy.ops.mesh.mark_seam()
    elif action == "clear_seam":
        bpy.ops.mesh.clear_seam()
    elif action == "mark_sharp":
        bpy.ops.mesh.mark_sharp()
    elif action == "crease":
        bpy.ops.transform.edge_crease(value=1.0)

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": f"edges_{action}"}


def edit_mesh_faces(params: dict) -> dict:
    obj_name = params["object_name"]
    action = params.get("action", "select")

    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    if action == "delete":
        bpy.ops.mesh.delete(type='FACE')
    elif action == "fill":
        bpy.ops.mesh.fill()
    elif action == "grid_fill":
        bpy.ops.mesh.grid_fill()
    elif action == "triangulate":
        bpy.ops.mesh.triangulate()
    elif action == "poke":
        bpy.ops.mesh.poke_faces()

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": f"faces_{action}"}


def create_vertex_group(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{params['object_name']}' not found"}
    vg = obj.vertex_groups.new(name=params["group_name"])
    return {"status": "vertex_group_created", "name": vg.name}


def assign_vertex_group(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    vg = obj.vertex_groups.get(params["group_name"])
    if not vg:
        return {"error": f"Vertex group '{params['group_name']}' not found"}
    vg.add(params["vertices"], params.get("weight", 1.0), 'REPLACE')
    return {"status": "assigned", "count": len(params["vertices"])}


def separate_by_material(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type='MATERIAL')
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "separated_by_material"}


def separate_by_loose(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "separated_by_loose"}


def smooth_vertices(params: dict) -> dict:
    obj_name = params["object_name"]
    factor = params.get("factor", 0.5)
    iterations = params.get("iterations", 1)
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.smooth_vertices(factor=factor, iterations=iterations)
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "smoothed", "factor": factor, "iterations": iterations}


def tri_to_quad(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.tris_to_quads(angle_limit=params.get("angle_limit", 0.698))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "tri_to_quad"}


def limited_dissolve(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_limited(angle_limit=params.get("angle_limit", 0.087))
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "dissolved"}


HANDLERS = {
    "edit_mesh_vertices": edit_mesh_vertices,
    "edit_mesh_edges": edit_mesh_edges,
    "edit_mesh_faces": edit_mesh_faces,
    "create_vertex_group": create_vertex_group,
    "assign_vertex_group": assign_vertex_group,
    "separate_by_material": separate_by_material,
    "separate_by_loose": separate_by_loose,
    "smooth_vertices": smooth_vertices,
    "tri_to_quad": tri_to_quad,
    "limited_dissolve": limited_dissolve,
}
