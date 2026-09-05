"""Physics handlers — rigid body, cloth, fluid, particles, force fields."""

import bpy


def add_rigid_body(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.rigidbody.object_add(type=params.get("body_type", "ACTIVE"))
    rb = obj.rigid_body
    rb.mass = params.get("mass", 1.0)
    rb.friction = params.get("friction", 0.5)
    rb.restitution = params.get("restitution", 0.0)
    return {"status": "rigid_body_added", "type": rb.type}


def add_cloth_physics(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='CLOTH')
    mod = obj.modifiers.get("Cloth")
    if mod:
        mod.settings.mass = params.get("mass", 0.3)
        mod.settings.tension_stiffness = params.get("tension", 15.0)
        mod.settings.compression_stiffness = params.get("compression", 0.5)
    return {"status": "cloth_added"}


def add_fluid_physics(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='FLUID')
    mod = obj.modifiers.get("Fluid")
    if mod:
        mod.fluid_type = params.get("domain_type", "DOMAIN")
    return {"status": "fluid_added"}


def add_particle_system(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.particle_system_add()
    ps = obj.particle_systems.active
    ps.settings.count = params.get("count", 1000)
    ps.settings.lifetime = params.get("lifetime", 50)
    ps.frame_start = params.get("frame_start", 1)
    ps.frame_end = params.get("frame_end", 250)
    return {"status": "particles_added", "count": ps.settings.count}


def add_force_field(params: dict) -> dict:
    name = params.get("name", "ForceField")
    field_type = params.get("field_type", "FORCE")
    location = params.get("location", (0, 0, 0))
    strength = params.get("strength", 1.0)
    bpy.ops.object.effector_add(type=field_type, location=location)
    effector = bpy.context.active_object
    effector.name = name
    effector.field.strength = strength
    effector.field.flow = params.get("flow", 0.0)
    return {"status": "force_field_added", "name": effector.name}


def bake_physics(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.ptcache.bake_all(bake=True)
    return {"status": "physics_baked"}


def delete_physics(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    if obj.rigid_body:
        bpy.ops.rigidbody.object_remove()
    for mod in list(obj.modifiers):
        if mod.type in ('CLOTH', 'FLUID', 'PARTICLE_SYSTEM', 'SOFT_BODY'):
            obj.modifiers.remove(mod)
    return {"status": "physics_deleted"}


HANDLERS = {
    "add_rigid_body": add_rigid_body,
    "add_cloth_physics": add_cloth_physics,
    "add_fluid_physics": add_fluid_physics,
    "add_particle_system": add_particle_system,
    "add_force_field": add_force_field,
    "bake_physics": bake_physics,
    "delete_physics": delete_physics,
}
