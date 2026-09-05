"""Handler registry — maps command types to handler functions."""

from . import (
    scene_handlers,
    object_handlers,
    transform_handlers,
    material_handlers,
    light_handlers,
    camera_handlers,
    modifier_handlers,
    mesh_handlers,
    animation_handlers,
    render_handlers,
    viewport_handlers,
    sculpt_handlers,
    uv_handlers,
    physics_handlers,
    geometry_nodes_handlers,
    curve_handlers,
    armature_handlers,
    collection_handlers,
    file_handlers,
    procedural_handlers,
    code_exec_handlers,
)

DISPATCHER = {}

def register_handlers():
    """Register all handlers into the global dispatcher."""
    DISPATCHER.update(scene_handlers.HANDLERS)
    DISPATCHER.update(object_handlers.HANDLERS)
    DISPATCHER.update(transform_handlers.HANDLERS)
    DISPATCHER.update(material_handlers.HANDLERS)
    DISPATCHER.update(light_handlers.HANDLERS)
    DISPATCHER.update(camera_handlers.HANDLERS)
    DISPATCHER.update(modifier_handlers.HANDLERS)
    DISPATCHER.update(mesh_handlers.HANDLERS)
    DISPATCHER.update(animation_handlers.HANDLERS)
    DISPATCHER.update(render_handlers.HANDLERS)
    DISPATCHER.update(viewport_handlers.HANDLERS)
    DISPATCHER.update(sculpt_handlers.HANDLERS)
    DISPATCHER.update(uv_handlers.HANDLERS)
    DISPATCHER.update(physics_handlers.HANDLERS)
    DISPATCHER.update(geometry_nodes_handlers.HANDLERS)
    DISPATCHER.update(curve_handlers.HANDLERS)
    DISPATCHER.update(armature_handlers.HANDLERS)
    DISPATCHER.update(collection_handlers.HANDLERS)
    DISPATCHER.update(file_handlers.HANDLERS)
    DISPATCHER.update(procedural_handlers.HANDLERS)
    DISPATCHER.update(code_exec_handlers.HANDLERS)

register_handlers()
