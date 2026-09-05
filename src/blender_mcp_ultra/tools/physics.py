"""Physics tools — rigid body, cloth, fluid, particles, force fields."""

from blender_mcp_ultra.connection import get_blender_connection
from blender_mcp_ultra.server import mcp
from blender_mcp_ultra.validators import Validator


@mcp.tool()
def add_rigid_body(
    object_name: str,
    body_type: str = "ACTIVE",
    mass: float = 1.0,
    friction: float = 0.5,
    restitution: float = 0.0,
) -> dict:
    """Add rigid body physics to an object.

    Args:
        object_name: Target object.
        body_type: ACTIVE (dynamic) or PASSIVE (static/kinematic).
        mass: Mass in kg.
        friction: Surface friction (0-1).
        restitution: Bounciness (0-1).
    """
    conn = get_blender_connection()
    return conn.send_command("add_rigid_body", {
        "object_name": Validator.validate_name(object_name),
        "body_type": body_type.upper(),
        "mass": Validator.validate_float(mass, 0.001, 100000),
        "friction": Validator.validate_percentage(friction) / 100.0,
        "restitution": Validator.validate_percentage(restitution) / 100.0,
    })


@mcp.tool()
def add_cloth_physics(
    object_name: str,
    quality_steps: int = 5,
    mass: float = 0.3,
    tension: float = 15.0,
    compression: float = 0.5,
) -> dict:
    """Add cloth simulation to an object.

    Args:
        object_name: Target object.
        quality_steps: Simulation quality (1-20).
        mass: Cloth mass density.
        tension: Structural tension.
        compression: Structural compression.
    """
    conn = get_blender_connection()
    return conn.send_command("add_cloth_physics", {
        "object_name": Validator.validate_name(object_name),
        "quality_steps": Validator.validate_int(quality_steps, 1, 20),
        "mass": Validator.validate_float(mass, 0.001, 100),
        "tension": Validator.validate_float(tension, 0, 1000),
        "compression": Validator.validate_float(compression, 0, 1000),
    })


@mcp.tool()
def add_fluid_physics(
    object_name: str,
    domain_type: str = "DOMAIN",
    fluid_type: str = "LIQUID",
) -> dict:
    """Add fluid simulation to an object.

    Args:
        object_name: Target object.
        domain_type: DOMAIN, EFFERENT, FLOW, or COLLISION.
        fluid_type: LIQUID or GAS.
    """
    conn = get_blender_connection()
    return conn.send_command("add_fluid_physics", {
        "object_name": Validator.validate_name(object_name),
        "domain_type": domain_type.upper(),
        "fluid_type": fluid_type.upper(),
    })


@mcp.tool()
def add_particle_system(
    object_name: str,
    particle_type: str = "EMITTER",
    count: int = 1000,
    lifetime: int = 50,
    frame_start: int = 1,
    frame_end: int = 250,
) -> dict:
    """Add a particle system to an object.

    Args:
        object_name: Target object.
        particle_type: EMITTER, HAIR, or STATIC_HAIR.
        count: Number of particles.
        lifetime: Particle lifetime in frames.
        frame_start: Start frame.
        frame_end: End frame.
    """
    conn = get_blender_connection()
    return conn.send_command("add_particle_system", {
        "object_name": Validator.validate_name(object_name),
        "particle_type": particle_type.upper(),
        "count": Validator.validate_int(count, 1, 10000000),
        "lifetime": Validator.validate_int(lifetime, 1, 100000),
        "frame_start": Validator.validate_int(frame_start, 0, 1000000),
        "frame_end": Validator.validate_int(frame_end, 1, 1000000),
    })


@mcp.tool()
def add_force_field(
    name: str = "ForceField",
    field_type: str = "FORCE",
    location: list[float] = None,
    strength: float = 1.0,
    flow: float = 0.0,
) -> dict:
    """Add a force field effect.

    Args:
        name: Force field name.
        field_type: FORCE, WIND, VORTEX, MAGNET, CHARGE, LENARD_JONES, TURBULENCE, etc.
        location: [x, y, z] position.
        strength: Field strength.
        flow: Field flow.
    """
    conn = get_blender_connection()
    params = {
        "name": Validator.validate_name(name),
        "field_type": field_type.upper(),
        "strength": Validator.validate_float(strength, -10000, 10000),
        "flow": Validator.validate_float(flow, -10, 10),
    }
    if location:
        params["location"] = Validator.validate_vector(location)
    return conn.send_command("add_force_field", params)


@mcp.tool()
def bake_physics(object_name: str, frame_start: int = 1, frame_end: int = 250) -> dict:
    """Bake physics simulation for an object.

    Args:
        object_name: Object with physics.
        frame_start: First frame to bake.
        frame_end: Last frame to bake.
    """
    conn = get_blender_connection()
    return conn.send_command("bake_physics", {
        "object_name": Validator.validate_name(object_name),
        "frame_start": Validator.validate_int(frame_start, 0, 1000000),
        "frame_end": Validator.validate_int(frame_end, 1, 1000000),
    })


@mcp.tool()
def delete_physics(object_name: str) -> dict:
    """Remove all physics from an object.

    Args:
        object_name: Target object.
    """
    conn = get_blender_connection()
    return conn.send_command("delete_physics", {"object_name": Validator.validate_name(object_name)})
