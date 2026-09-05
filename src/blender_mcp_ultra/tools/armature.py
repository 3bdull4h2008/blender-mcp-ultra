"""Armature/rigging tools — bones, armatures, constraints."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def create_armature(
    name: str = "Armature",
    location: list[float] = None,
) -> dict:
    """Create a new armature object.

    Args:
        name: Armature name.
        location: [x, y, z] position.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(name)}
    if location:
        params["location"] = Validator.validate_vector(location)
    return conn.send_command("create_armature", params)


@mcp.tool()
def add_bone(
    armature_name: str,
    bone_name: str,
    head: list[float] = None,
    tail: list[float] = None,
    parent_bone: str = "",
) -> dict:
    """Add a bone to an armature.

    Args:
        armature_name: Target armature.
        bone_name: Name for the bone.
        head: [x, y, z] bone head position.
        tail: [x, y, z] bone tail position.
        parent_bone: Parent bone name (for hierarchy).
    """
    conn = get_blender_connection()
    params = {
        "armature_name": Validator.validate_name(armature_name),
        "bone_name": Validator.validate_name(bone_name),
    }
    if head:
        params["head"] = Validator.validate_vector(head)
    if tail:
        params["tail"] = Validator.validate_vector(tail)
    if parent_bone:
        params["parent_bone"] = Validator.validate_name(parent_bone)
    return conn.send_command("add_bone", params)


@mcp.tool()
def create_humanoid_rig(
    armature_name: str = "HumanRig",
    location: list[float] = None,
) -> dict:
    """Create a basic humanoid armature with spine, arms, and legs.

    Args:
        armature_name: Name for the armature.
        location: [x, y, z] position.
    """
    conn = get_blender_connection()
    params = {"name": Validator.validate_name(armature_name)}
    if location:
        params["location"] = Validator.validate_vector(location)
    return conn.send_command("create_humanoid_rig", params)


@mcp.tool()
def add_bone_constraint(
    armature_name: str,
    bone_name: str,
    constraint_type: str = "TRACK_TO",
    target_name: str = "",
    **kwargs,
) -> dict:
    """Add a constraint to a bone.

    Args:
        armature_name: Target armature.
        bone_name: Bone to constrain.
        constraint_type: TRACK_TO, COPY_LOCATION, COPY_ROTATION, IK, etc.
        target_name: Target object for the constraint.
    """
    conn = get_blender_connection()
    params = {
        "armature_name": Validator.validate_name(armature_name),
        "bone_name": Validator.validate_name(bone_name),
        "constraint_type": constraint_type.upper(),
    }
    if target_name:
        params["target_name"] = Validator.validate_name(target_name)
    params.update(kwargs)
    return conn.send_command("add_bone_constraint", params)


@mcp.tool()
def setup_ik_chain(
    armature_name: str,
    chain_bones: list[str],
    pole_target: str = "",
) -> dict:
    """Set up an IK (Inverse Kinematics) chain.

    Args:
        armature_name: Target armature.
        chain_bones: List of bone names in the chain.
        pole_target: Pole target object name.
    """
    conn = get_blender_connection()
    params = {
        "armature_name": Validator.validate_name(armature_name),
        "chain_bones": [Validator.validate_name(b) for b in chain_bones],
    }
    if pole_target:
        params["pole_target"] = Validator.validate_name(pole_target)
    return conn.send_command("setup_ik_chain", params)


@mcp.tool()
def parent_bone_to_object(
    armature_name: str,
    bone_name: str,
    object_name: str,
) -> dict:
    """Parent an object to a bone (for rigging).

    Args:
        armature_name: Target armature.
        bone_name: Bone to parent to.
        object_name: Object to parent.
    """
    conn = get_blender_connection()
    return conn.send_command("parent_bone_to_object", {
        "armature_name": Validator.validate_name(armature_name),
        "bone_name": Validator.validate_name(bone_name),
        "object_name": Validator.validate_name(object_name),
    })
