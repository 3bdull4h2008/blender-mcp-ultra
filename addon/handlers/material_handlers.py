"""Material handlers — create, assign, configure materials and shader nodes."""

import bpy


def create_material(params: dict) -> dict:
    name = params.get("name", "Material")
    color = params.get("color", [0.8, 0.8, 0.8, 1.0])
    metallic = params.get("metallic", 0.0)
    roughness = params.get("roughness", 0.5)

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return {"status": "created", "name": mat.name}


def assign_material(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    mat = bpy.data.materials.get(params["material_name"])
    if not mat:
        return {"error": f"Material '{params['material_name']}' not found"}
    slot = params.get("slot", 0)
    if len(obj.material_slots) <= slot:
        obj.data.materials.append(mat)
    else:
        obj.material_slots[slot].material = mat
    return {"status": "assigned", "object": obj.name, "material": mat.name, "slot": slot}


def delete_material(params: dict) -> dict:
    obj = bpy.data.objects.get(params["object_name"])
    if not obj:
        return {"error": f"Object '{params['object_name']}' not found"}
    slot = params.get("slot", 0)
    if slot < len(obj.material_slots):
        obj.data.materials.pop(index=slot)
        return {"status": "removed", "object": obj.name, "slot": slot}
    return {"error": f"Material slot {slot} not found"}


def set_material_property(params: dict) -> dict:
    mat_name = params["material_name"]
    prop = params["property_name"]
    value = params["value"]
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        return {"error": f"Material '{mat_name}' not found"}
    if not mat.use_nodes:
        return {"error": "Material must use nodes"}
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if not bsdf:
        return {"error": "Principled BSDF node not found"}
    if prop in bsdf.inputs:
        input_node = bsdf.inputs[prop]
        if isinstance(value, list):
            input_node.default_value = value
        else:
            input_node.default_value = value
        return {"status": "set", "material": mat_name, "property": prop, "value": str(value)}
    return {"error": f"Input '{prop}' not found on Principled BSDF"}


def create_procedural_material(params: dict) -> dict:
    name = params.get("name", "ProceduralMaterial")
    pattern = params.get("pattern", "noise")
    color1 = params.get("color1", [0.2, 0.2, 0.2])
    color2 = params.get("color2", [0.8, 0.8, 0.8])
    scale = params.get("scale", 1.0)
    detail = params.get("detail", 6.0)
    roughness = params.get("roughness", 0.5)

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    tree = mat.node_tree
    nodes = tree.nodes
    links = tree.links

    # Clear default nodes
    for n in nodes:
        nodes.remove(n)

    # Create nodes
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-400, 0)
    mapping.inputs['Scale'].default_value = (scale, scale, scale)

    # Texture node based on pattern
    pattern_map = {
        "noise": 'ShaderNodeTexNoise',
        "voronoi": 'ShaderNodeTexVoronoi',
        "musgrave": 'ShaderNodeTexMusgrave',
        "wave": 'ShaderNodeTexWave',
        "magic": 'ShaderNodeTexMagic',
        "checker": 'ShaderNodeTexChecker',
        "gradient": 'ShaderNodeTexGradient',
        "brick": 'ShaderNodeTexBrick',
    }
    tex_node_class = pattern_map.get(pattern, 'ShaderNodeTexNoise')
    tex_node = nodes.new(tex_node_class)
    tex_node.location = (-200, 0)
    if hasattr(tex_node.inputs, 'Scale'):
        tex_node.inputs['Scale'].default_value = scale
    if hasattr(tex_node.inputs, 'Detail'):
        tex_node.inputs['Detail'].default_value = detail
    if hasattr(tex_node.inputs, 'Roughness'):
        tex_node.inputs['Roughness'].default_value = roughness

    # Color ramp
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (0, 0)
    ramp.color_ramp.elements[0].color = (*color1, 1.0)
    ramp.color_ramp.elements[1].color = (*color2, 1.0)

    # Principled BSDF
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Roughness'].default_value = roughness

    # Output
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)

    # Connect
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], tex_node.inputs['Vector'])
    links.new(tex_node.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    return {"status": "created", "name": mat.name, "pattern": pattern}


def add_shader_node(params: dict) -> dict:
    mat_name = params["material_name"]
    node_type = params["node_type"]
    location = params.get("location", [0, 0])
    label = params.get("name", "")
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        return {"error": f"Material '{mat_name}' not found"}
    if not mat.use_nodes:
        mat.use_nodes = True
    node = mat.node_tree.nodes.new(type=node_type)
    node.location = location
    if label:
        node.label = label
    return {"status": "node_added", "material": mat_name, "node_type": node_type, "label": node.label or node.name}


def connect_shader_nodes(params: dict) -> dict:
    mat_name = params["material_name"]
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        return {"error": f"Material '{mat_name}' not found"}
    from_node_name = params["from_node"]
    to_node_name = params["to_node"]
    from_socket = params["from_socket"]
    to_socket = params["to_socket"]

    from_node = None
    to_node = None
    for n in mat.node_tree.nodes:
        if n.name == from_node_name or n.label == from_node_name:
            from_node = n
        if n.name == to_node_name or n.label == to_node_name:
            to_node = n

    if not from_node:
        return {"error": f"Source node '{from_node_name}' not found"}
    if not to_node:
        return {"error": f"Target node '{to_node_name}' not found"}

    mat.node_tree.links.new(from_node.outputs[from_socket], to_node.inputs[to_socket])
    return {"status": "connected", "from": from_node_name, "to": to_node_name}


def set_shader_node_value(params: dict) -> dict:
    mat_name = params["material_name"]
    node_name = params["node_name"]
    input_name = params.get("input_name", "")
    value = params["value"]
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        return {"error": f"Material '{mat_name}' not found"}
    for n in mat.node_tree.nodes:
        if n.name == node_name or n.label == node_name:
            if input_name:
                if input_name in n.inputs:
                    n.inputs[input_name].default_value = value
                    return {"status": "value_set", "node": node_name, "input": input_name}
                return {"error": f"Input '{input_name}' not found on node '{node_name}'"}
            for inp in n.inputs:
                if hasattr(inp, 'default_value'):
                    inp.default_value = value
                    return {"status": "value_set", "node": node_name, "input": inp.name}
    return {"error": f"Node '{node_name}' not found"}


def apply_image_texture(params: dict) -> dict:
    obj_name = params["object_name"]
    image_path = params["image_path"]
    mat_name = params.get("material_name", "")

    obj = bpy.data.objects.get(obj_name)
    if not obj:
        return {"error": f"Object '{obj_name}' not found"}

    img = bpy.data.images.load(image_path)
    mat = bpy.data.materials.get(mat_name) if mat_name else None
    if not mat:
        mat = bpy.data.materials.new(name=f"{obj_name}_mat")
        mat.use_nodes = True

    tree = mat.node_tree
    bsdf = tree.nodes.get("Principled BSDF")
    tex_node = tree.nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

    if len(obj.material_slots) == 0:
        obj.data.materials.append(mat)
    else:
        obj.material_slots[0].material = mat

    return {"status": "texture_applied", "object": obj_name, "material": mat.name}


def list_materials(params: dict) -> dict:
    materials = []
    for mat in bpy.data.materials:
        materials.append({
            "name": mat.name,
            "users": mat.users,
            "use_nodes": mat.use_nodes,
        })
    return {"materials": materials, "count": len(materials)}


HANDLERS = {
    "create_material": create_material,
    "assign_material": assign_material,
    "delete_material": delete_material,
    "set_material_property": set_material_property,
    "create_procedural_material": create_procedural_material,
    "add_shader_node": add_shader_node,
    "connect_shader_nodes": connect_shader_nodes,
    "set_shader_node_value": set_shader_node_value,
    "apply_image_texture": apply_image_texture,
    "list_materials": list_materials,
}
