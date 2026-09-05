"""Mesh quality analysis handlers — detect defects, measure topology."""

import bpy
import bmesh


def analyze_mesh_quality(params: dict) -> dict:
    obj_name = params["object_name"]
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    defects = {
        "non_manifold_edges": len([e for e in bm.edges if not e.is_manifold]),
        "boundary_edges": len([e for e in bm.edges if e.is_boundary]),
        "loose_vertices": len([v for v in bm.verts if not v.link_edges]),
        "zero_area_faces": sum(1 for f in bm.faces if f.calc_area() < 1e-10),
        "duplicate_vertices": 0,
        "wire_edges": len([e for e in bm.edges if e.is_wire]),
        "twisted_faces": sum(1 for f in bm.faces if len(f.verts) == 4 and _is_twisted(f)),
    }

    # Check for duplicates
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bm2 = bmesh.new()
    bm2.from_mesh(mesh)
    bm2.edges.ensure_lookup_table()
    bm2.verts.ensure_lookup_table()
    duplicates = len(mesh.verts) - len(bm2.verts)
    defects["duplicate_vertices"] = max(0, duplicates)

    bm.free()
    bm2.free()

    total_defects = sum(v for v in defects.values() if isinstance(v, (int, float)))
    is_manifold = defects["non_manifold_edges"] == 0 and defects["boundary_edges"] == 0

    return {
        "object": obj_name,
        "defects": defects,
        "total_defects": total_defects,
        "is_manifold": is_manifold,
        "quality_score": max(0, 100 - total_defects * 2),
        "verdict": "CLEAN" if total_defects == 0 else "NEEDS_FIX" if total_defects < 10 else "POOR",
    }


def _is_twisted(face):
    if len(face.verts) != 4:
        return False
    v = [v.co for v in face.verts]
    e1 = v[1] - v[0]
    e2 = v[3] - v[2]
    cross = e1.cross(e2)
    return cross.length > 0.001


def get_mesh_statistics(params: dict) -> dict:
    obj_name = params["object_name"]
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    mesh = obj.data
    verts = len(mesh.vertices)
    edges = len(mesh.edges)
    faces = len(mesh.polygons)
    tris = sum(1 for f in mesh.polygons if len(f.vertices) == 3)
    quads = sum(1 for f in mesh.polygons if len(f.vertices) == 4)
    ngons = sum(1 for f in mesh.polygons if len(f.vertices) > 4)

    # Volume and surface area
    volume = 0.0
    area = 0.0
    if mesh.polygons:
        bm = bmesh.new()
        bm.from_mesh(mesh)
        volume = bm.calc_volume()
        area = sum(f.calc_area() for f in bm.faces)
        bm.free()

    dims = obj.dimensions
    return {
        "object": obj_name,
        "vertex_count": verts,
        "edge_count": edges,
        "face_count": faces,
        "triangle_count": tris,
        "quad_count": quads,
        "ngon_count": ngons,
        "volume": round(volume, 4),
        "surface_area": round(area, 4),
        "dimensions": {"x": round(dims.x, 4), "y": round(dims.y, 4), "z": round(dims.z, 4)},
        "complexity_tier": "SIMPLE" if verts < 1000 else "MODERATE" if verts < 10000 else "COMPLEX" if verts < 100000 else "HIGH_POLY",
    }


def check_manifold(params: dict) -> dict:
    obj_name = params["object_name"]
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    non_manifold = len([e for e in bm.edges if not e.is_manifold])
    boundary = len([e for e in bm.edges if e.is_boundary])
    bm.free()

    return {
        "object": obj_name,
        "is_manifold": non_manifold == 0 and boundary == 0,
        "non_manifold_edges": non_manifold,
        "boundary_edges": boundary,
    }


def get_geometry_complexity(params: dict) -> dict:
    stats = get_mesh_statistics(params)
    if "error" in stats:
        return stats
    return {
        "object": stats["object"],
        "triangles": stats["triangle_count"],
        "vertices": stats["vertex_count"],
        "ngons": stats["ngon_count"],
        "complexity_tier": stats["complexity_tier"],
    }


def check_production_readiness(params: dict) -> dict:
    obj_name = params["object_name"]
    obj = bpy.data.objects.get(obj_name)
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{obj_name}' not found"}

    score = 0
    checks = {}

    # Manifold check
    manifold = check_manifold(params)
    checks["manifold"] = manifold.get("is_manifold", False)
    if checks["manifold"]:
        score += 25

    # UV check
    has_uvs = len(obj.data.uv_layers) > 0
    checks["has_uvs"] = has_uvs
    if has_uvs:
        score += 25

    # Material check
    has_materials = len(obj.material_slots) > 0 and any(s.material for s in obj.material_slots)
    checks["has_materials"] = has_materials
    if has_materials:
        score += 25

    # Naming check
    is_named = not obj.name.startswith("Cube") and not obj.name.startswith("Plane")
    checks["has_descriptive_name"] = is_named
    if is_named:
        score += 12.5

    # Origin check
    origin_at_center = all(abs(obj.location[i]) < 0.01 for i in range(3))
    checks["origin_aligned"] = origin_at_center
    if origin_at_center:
        score += 12.5

    return {
        "object": obj_name,
        "score": round(score),
        "checks": checks,
        "verdict": "PRODUCTION_READY" if score >= 75 else "NEEDS_WORK" if score >= 50 else "NOT_READY",
    }


def find_duplicates(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{params['object_name']}' not found"}
    distance = params.get("distance", 0.001)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    result = bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=distance)
    removed = result.get("geom", [])
    bm.free()
    return {"duplicates_found": len(removed), "distance": distance}


def fix_mesh_defects(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj or obj.type != 'MESH':
        return {"error": f"Mesh object '{params['object_name']}' not found"}

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    fixes = []
    # Merge doubles
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    dist = params.get("merge_distance", 0.001)
    bpy.ops.mesh.remove_doubles(threshold=dist)
    fixes.append("merged_doubles")

    if params.get("fix_manifold", True):
        bpy.ops.mesh.normals_make_consistent(inside=False)
        fixes.append("fixed_normals")

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "defects_fixed", "fixes_applied": fixes}


HANDLERS = {
    "analyze_mesh_quality": analyze_mesh_quality,
    "get_mesh_statistics": get_mesh_statistics,
    "check_manifold": check_manifold,
    "get_geometry_complexity": get_geometry_complexity,
    "check_production_readiness": check_production_readiness,
    "find_duplicates": find_duplicates,
    "fix_mesh_defects": fix_mesh_defects,
}
