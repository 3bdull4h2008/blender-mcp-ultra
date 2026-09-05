"""Procedural generation handlers — terrain, trees, rocks."""

import bpy
import bmesh
import math
import random


def create_terrain(params: dict) -> dict:
    name = params.get("name", "Terrain")
    size = params.get("size", 10.0)
    subdivisions = params.get("subdivisions", 128)
    height = params.get("height", 1.0)
    seed = params.get("seed", 0)
    noise_scale = params.get("noise_scale", 2.0)

    bpy.ops.mesh.primitive_plane_add(size=size)
    obj = bpy.context.active_object
    obj.name = name

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=subdivisions)
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Displace vertices using noise-like pattern
    rng = random.Random(seed)
    for v in obj.data.vertices:
        x, y = v.co.x, v.co.y
        noise_val = sum(
            math.sin(x * ns * noise_scale + rng.random() * math.pi * 2) *
            math.cos(y * ns * noise_scale + rng.random() * math.pi * 2)
            for ns in [1.0, 2.0, 4.0, 0.5]
        ) / 4.0
        v.co.z = noise_val * height

    return {"status": "terrain_created", "name": obj.name, "vertices": len(obj.data.vertices)}


def create_tree(params: dict) -> dict:
    name = params.get("name", "Tree")
    trunk_height = params.get("trunk_height", 3.0)
    trunk_radius = params.get("trunk_radius", 0.15)
    seed = params.get("seed", 0)

    rng = random.Random(seed)

    # Trunk
    bpy.ops.mesh.primitive_cylinder_add(radius=trunk_radius, depth=trunk_height, location=(0, 0, trunk_height / 2))
    trunk = bpy.context.active_object
    trunk.name = f"{name}_Trunk"

    # Canopy (sphere with noise)
    canopy_size = trunk_height * 0.6
    bpy.ops.mesh.primitive_uv_sphere_add(radius=canopy_size, location=(0, 0, trunk_height * 0.85))
    canopy = bpy.context.active_object
    canopy.name = f"{name}_Canopy"

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(canopy.data)
    for v in bm.verts:
        noise = sum(rng.uniform(-0.1, 0.1) for _ in range(3))
        v.co *= 1.0 + noise
    bmesh.update_edit_mesh(canopy.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Leaf material
    mat = bpy.data.materials.new(name=f"{name}_LeafMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.1, 0.5, 0.1, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.8
    canopy.data.materials.append(mat)

    # Join
    bpy.ops.object.select_all(action='DESELECT')
    trunk.select_set(True)
    canopy.select_set(True)
    bpy.context.view_layer.objects.active = trunk
    bpy.ops.object.join()
    trunk.name = name

    return {"status": "tree_created", "name": trunk.name}


def create_rock(params: dict) -> dict:
    name = params.get("name", "Rock")
    size = params.get("size", 1.0)
    detail = params.get("detail", 0.5)
    roughness = params.get("roughness", 0.8)
    seed = params.get("seed", 0)

    rng = random.Random(seed)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=size, subdivisions=3)
    obj = bpy.context.active_object
    obj.name = name

    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        noise = sum(rng.uniform(-detail, detail) for _ in range(3))
        v.co *= 1.0 + noise
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Material
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        gray = rng.uniform(0.3, 0.6)
        bsdf.inputs["Base Color"].default_value = (gray, gray * 0.95, gray * 0.9, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
    obj.data.materials.append(mat)

    return {"status": "rock_created", "name": obj.name}


def create_particle_field(params: dict) -> dict:
    name = params.get("name", "ParticleField")
    count = params.get("count", 100)
    size = params.get("size", 5.0)
    seed = params.get("seed", 0)

    rng = random.Random(seed)
    objs = []
    for i in range(count):
        x = rng.uniform(-size / 2, size / 2)
        y = rng.uniform(-size / 2, size / 2)
        z = rng.uniform(0, size * 0.3)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.05, location=(x, y, z))
        obj = bpy.context.active_object
        obj.name = f"{name}_{i:04d}"
        objs.append(obj)

    return {"status": "field_created", "count": len(objs)}


HANDLERS = {
    "create_terrain": create_terrain,
    "create_tree": create_tree,
    "create_rock": create_rock,
    "create_particle_field": create_particle_field,
}
