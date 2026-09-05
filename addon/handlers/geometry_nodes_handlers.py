"""Geometry Nodes handlers."""

import bpy


def add_geometry_nodes_modifier(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='NODES')
    mod = obj.modifiers.get("GeometryNodes")
    if mod:
        group_name = params.get("node_group_name", "GeometryNodes")
        node_group = bpy.data.node_groups.new(group_name, 'GeometryNodeTree')
        mod.node_group = node_group
    return {"status": "geometry_nodes_added", "object": obj.name}


def add_geometry_node(params: dict) -> dict:
    group_name = params["node_group_name"]
    node_type = params["node_type"]
    location = params.get("location", [0, 0])
    group = bpy.data.node_groups.get(group_name)
    if not group:
        return {"error": f"Node group '{group_name}' not found"}
    node = group.nodes.new(type=node_type)
    node.location = location
    return {"status": "node_added", "type": node_type, "name": node.name}


def connect_geometry_nodes(params: dict) -> dict:
    group_name = params["node_group_name"]
    group = bpy.data.node_groups.get(group_name)
    if not group:
        return {"error": f"Node group '{group_name}' not found"}
    from_node_name = params["from_node"]
    to_node_name = params["to_node"]
    from_socket = params["from_socket"]
    to_socket = params["to_socket"]
    from_node = None
    to_node = None
    for n in group.nodes:
        if n.name == from_node_name or n.label == from_node_name:
            from_node = n
        if n.name == to_node_name or n.label == to_node_name:
            to_node = n
    if not from_node:
        return {"error": f"Source node '{from_node_name}' not found"}
    if not to_node:
        return {"error": f"Target node '{to_node_name}' not found"}
    group.links.new(from_node.outputs[from_socket], to_node.inputs[to_socket])
    return {"status": "connected"}


def create_procedural_distribution(params: dict) -> dict:
    obj_name = params["object_name"]
    instance_name = params.get("instance_object", "")
    count = params.get("count", 100)

    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_add(type='NODES')
    mod = obj.modifiers.get("GeometryNodes")
    group = bpy.data.node_groups.new("Distribution", 'GeometryNodeTree')
    mod.node_group = group

    # Create basic distribution nodes
    input_node = group.nodes.new('NodeGroupInput')
    input_node.location = (-400, 0)

    distribute = group.nodes.new('GeometryNodeDistributePointsOnFaces')
    distribute.location = (-200, 0)
    distribute.inputs['Density'].default_value = count

    output_node = group.nodes.new('NodeGroupOutput')
    output_node.location = (0, 0)

    group.links.new(input_node.outputs[0], distribute.inputs['Mesh'])
    group.links.new(distribute.outputs['Points'], output_node.inputs[0])

    return {"status": "distribution_created", "count": count}


HANDLERS = {
    "add_geometry_nodes_modifier": add_geometry_nodes_modifier,
    "add_geometry_node": add_geometry_node,
    "connect_geometry_nodes": connect_geometry_nodes,
    "create_procedural_distribution": create_procedural_distribution,
}
