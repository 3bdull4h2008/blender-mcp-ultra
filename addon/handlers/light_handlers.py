"""Light handlers — create and configure lights."""

import bpy
import math


def create_light(params: dict) -> dict:
    name = params.get("name", "Light")
    light_type = params.get("light_type", "POINT")
    location = params.get("location", (0, 0, 3))
    energy = params.get("energy", 1000.0)
    color = params.get("color", [1.0, 1.0, 1.0])
    radius = params.get("radius", 0.0)

    type_map = {"POINT": 'POINT', "SUN": 'SUN', "SPOT": 'SPOT', "AREA": 'AREA'}
    bpy.ops.object.light_add(type=type_map.get(light_type, 'POINT'), location=location)
    light = bpy.context.active_object
    light.name = name
    light.data.energy = energy
    light.data.color = color
    if radius > 0:
        light.data.shadow_soft_size = radius
    return {"status": "created", "name": light.name, "type": light_type}


def configure_light(params: dict) -> dict:
    name = params["name"]
    obj = bpy.data.objects.get(name)
    if not obj or obj.type != 'LIGHT':
        return {"error": f"Light '{name}' not found"}
    data = obj.data
    if "energy" in params:
        data.energy = params["energy"]
    if "color" in params:
        data.color = params["color"]
    if "radius" in params:
        data.shadow_soft_size = params["radius"]
    if "spot_angle" in params:
        data.spot_size = params["spot_angle"]
    if "shadow_soft_size" in params:
        data.shadow_soft_size = params["shadow_soft_size"]
    return {"status": "configured", "name": name}


def setup_three_point_lighting(params: dict) -> dict:
    key_energy = params.get("key_energy", 1000)
    fill_energy = params.get("fill_energy", 300)
    rim_energy = params.get("rim_energy", 500)
    key_color = params.get("key_color", [1.0, 0.95, 0.9])
    fill_color = params.get("fill_color", [0.9, 0.95, 1.0])
    rim_color = params.get("rim_color", [1.0, 1.0, 1.0])
    dist = params.get("distance", 5.0)

    # Key light
    bpy.ops.object.light_add(type='AREA', location=(dist, -dist, dist * 0.75))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = key_energy
    key.data.color = key_color
    key.data.size = 2.0
    key.rotation_euler = (math.radians(45), 0, math.radians(45))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-dist * 0.8, -dist * 0.5, dist * 0.5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = fill_energy
    fill.data.color = fill_color
    fill.data.size = 3.0
    fill.rotation_euler = (math.radians(60), 0, math.radians(-30))

    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, dist, dist * 0.5))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = rim_energy
    rim.data.color = rim_color
    rim.data.size = 1.5
    rim.rotation_euler = (math.radians(70), 0, math.radians(180))

    return {"status": "three_point_lighting_setup", "lights": ["Key_Light", "Fill_Light", "Rim_Light"]}


def setup_hdri_lighting(params: dict) -> dict:
    hdri_path = params.get("hdri_path", "")
    strength = params.get("strength", 1.0)
    rotation = params.get("rotation", 0.0)

    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    tree = world.node_tree
    nodes = tree.nodes
    links = tree.links

    nodes.clear()
    output = nodes.new('ShaderNodeOutputWorld')
    output.location = (300, 0)

    if hdri_path:
        env_tex = nodes.new('ShaderNodeTexEnvironment')
        env_tex.image = bpy.data.images.load(hdri_path)
        env_tex.location = (-200, 0)
        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-400, 0)
        mapping.inputs['Rotation'].default_value = (0, 0, rotation)
        links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
        links.new(env_tex.outputs['Color'], output.inputs['Surface'])
    else:
        bg = nodes.new('ShaderNodeBackground')
        bg.inputs['Strength'].default_value = strength
        bg.location = (100, 0)
        links.new(bg.outputs['Background'], output.inputs['Surface'])

    return {"status": "hdri_setup", "has_hdri": bool(hdri_path)}


def setup_studio_lighting(params: dict) -> dict:
    style = params.get("style", "STUDIO")
    key_energy = params.get("key_energy", 1000)

    # Remove existing lights
    for obj in list(bpy.context.scene.objects):
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

    if style == "PORTRAIT":
        return setup_three_point_lighting({"key_energy": key_energy, "distance": 3.0})
    elif style == "PRODUCT":
        return setup_three_point_lighting({"key_energy": key_energy * 1.2, "distance": 2.5})
    elif style == "DRAMATIC":
        bpy.ops.object.light_add(type='SPOT', location=(3, -3, 4))
        light = bpy.context.active_object
        light.name = "Dramatic_Spot"
        light.data.energy = key_energy * 2
        return {"status": "studio_setup", "style": style, "lights": ["Dramatic_Spot"]}
    else:
        return setup_three_point_lighting({"key_energy": key_energy})


def set_world_environment(params: dict) -> dict:
    color = params.get("color", [0.5, 0.5, 0.5])
    strength = params.get("strength", 1.0)

    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    tree = world.node_tree
    bg = tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (*color, 1.0)
        bg.inputs['Strength'].default_value = strength
    return {"status": "world_set"}


def list_lights(params: dict) -> dict:
    lights = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT':
            lights.append({
                "name": obj.name,
                "type": obj.data.type,
                "energy": obj.data.energy,
                "color": list(obj.data.color),
                "location": list(obj.location),
            })
    return {"lights": lights, "count": len(lights)}


HANDLERS = {
    "create_light": create_light,
    "configure_light": configure_light,
    "setup_three_point_lighting": setup_three_point_lighting,
    "setup_hdri_lighting": setup_hdri_lighting,
    "setup_studio_lighting": setup_studio_lighting,
    "set_world_environment": set_world_environment,
    "list_lights": list_lights,
}
