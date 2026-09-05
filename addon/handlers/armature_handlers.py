"""Armature/rigging handlers."""

import bpy


def create_armature(params: dict) -> dict:
    name = params.get("name", "Armature")
    location = params.get("location", (0, 0, 0))
    bpy.ops.object.armature_add(location=location)
    arm = bpy.context.active_object
    arm.name = name
    bpy.ops.object.mode_set(mode='EDIT')
    # Remove default bone
    if arm.data.bones:
        arm.data.edit_bones.remove(arm.data.edit_bones[0])
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "created", "name": arm.name}


def add_bone(params: dict) -> dict:
    arm_name = params["armature_name"]
    bone_name = params["bone_name"]
    head = params.get("head", (0, 0, 0))
    tail = params.get("tail", (0, 0, 1))
    parent_name = params.get("parent_bone", "")

    arm_obj = bpy.data.objects.get(arm_name)
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return {"error": f"Armature '{arm_name}' not found"}

    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bone = arm_obj.data.edit_bones.new(bone_name)
    bone.head = head
    bone.tail = tail
    if parent_name:
        parent = arm_obj.data.edit_bones.get(parent_name)
        if parent:
            bone.parent = parent
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "bone_added", "name": bone_name}


def create_humanoid_rig(params: dict) -> dict:
    name = params.get("name", "HumanRig")
    location = params.get("location", (0, 0, 0))

    bpy.ops.object.armature_add(location=location)
    arm = bpy.context.active_object
    arm.name = name

    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm.data.edit_bones

    # Remove default bone
    for b in list(eb):
        eb.remove(b)

    # Spine
    spine = eb.new("Spine")
    spine.head = (0, 0, 0.9)
    spine.tail = (0, 0, 1.1)

    chest = eb.new("Chest")
    chest.head = spine.tail
    chest.tail = (0, 0, 1.4)
    chest.parent = spine

    neck = eb.new("Neck")
    neck.head = chest.tail
    neck.tail = (0, 0, 1.55)
    neck.parent = chest

    head = eb.new("Head")
    head.head = neck.tail
    head.tail = (0, 0, 1.75)
    head.parent = neck

    # Arms
    for side, x in [("L", -0.2), ("L.001", -0.5)]:
        shoulder = eb.new(f"Shoulder_{side}")
        shoulder.head = (x, 0, 1.35)
        shoulder.tail = (x - 0.3, 0, 1.3)
        shoulder.parent = chest

    # Legs
    for side, x in [("L", -0.1), ("L.001", -0.1)]:
        thigh = eb.new(f"Thigh_{side}")
        thigh.head = (x, 0, 0.85)
        thigh.tail = (x, 0, 0.45)
        thigh.parent = spine

    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": "humanoid_rig_created", "name": arm.name}


def add_bone_constraint(params: dict) -> dict:
    arm_name = params["armature_name"]
    bone_name = params["bone_name"]
    constraint_type = params.get("constraint_type", "TRACK_TO")

    arm_obj = bpy.data.objects.get(arm_name)
    if not arm_obj:
        return {"error": f"Armature '{arm_name}' not found"}

    bone = arm_obj.pose.bones.get(bone_name)
    if not bone:
        return {"error": f"Bone '{bone_name}' not found"}

    constraint = bone.constraints.new(type=constraint_type)
    target_name = params.get("target_name", "")
    if target_name:
        target = bpy.data.objects.get(target_name)
        if target:
            constraint.target = target
    return {"status": "constraint_added", "bone": bone_name, "type": constraint_type}


def setup_ik_chain(params: dict) -> dict:
    arm_name = params["armature_name"]
    chain_bones = params.get("chain_bones", [])
    if len(chain_bones) < 2:
        return {"error": "IK chain needs at least 2 bones"}

    arm_obj = bpy.data.objects.get(arm_name)
    if not arm_obj:
        return {"error": f"Armature '{arm_name}' not found"}

    bone = arm_obj.pose.bones.get(chain_bones[-1])
    if not bone:
        return {"error": f"Bone '{chain_bones[-1]}' not found"}

    ik = bone.constraints.new(type='IK')
    ik.chain_length = len(chain_bones) - 1

    pole_name = params.get("pole_target", "")
    if pole_name:
        pole = bpy.data.objects.get(pole_name)
        if pole:
            ik.target = pole

    return {"status": "ik_chain_set", "chain_length": ik.chain_length}


def parent_bone_to_object(params: dict) -> dict:
    arm_name = params["armature_name"]
    bone_name = params["bone_name"]
    obj_name = params["object_name"]

    arm_obj = bpy.data.objects.get(arm_name)
    obj = bpy.data.objects.get(obj_name)
    if not arm_obj or not obj:
        return {"error": "Armature or object not found"}

    obj.parent = arm_obj
    obj.parent_type = 'BONE'
    obj.parent_bone = bone_name
    return {"status": "parented_to_bone", "object": obj_name, "bone": bone_name}


HANDLERS = {
    "create_armature": create_armature,
    "add_bone": add_bone,
    "create_humanoid_rig": create_humanoid_rig,
    "add_bone_constraint": add_bone_constraint,
    "setup_ik_chain": setup_ik_chain,
    "parent_bone_to_object": parent_bone_to_object,
}
