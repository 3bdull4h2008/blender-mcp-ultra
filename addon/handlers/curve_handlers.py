"""Curve handlers — create and edit curves and text objects."""

import bpy


def create_curve(params: dict) -> dict:
    name = params.get("name", "Curve")
    curve_type = params.get("curve_type", "BEZIER")
    location = params.get("location", (0, 0, 0))
    bevel_depth = params.get("bevel_depth", 0.0)

    if curve_type == "NURBS":
        bpy.ops.curve.primitive_nurbs_circle_add(location=location)
    else:
        bpy.ops.curve.primitive_bezier_circle_add(location=location)

    obj = bpy.context.active_object
    obj.name = name
    obj.data.bevel_depth = bevel_depth
    obj.data.bevel_resolution = params.get("bevel_resolution", 0)
    fill_map = {"FULL": 'FULL', "HALF": 'HALF', "NONE": 'NONE'}
    obj.data.fill_mode = fill_map.get(params.get("fill", "FULL"), 'FULL')

    points = params.get("points")
    if points and len(points) >= 2:
        spline = obj.data.splines[0]
        spline.bezier_points.add(len(points) - len(spline.bezier_points))
        for i, pt in enumerate(points):
            if i < len(spline.bezier_points):
                spline.bezier_points[i].co = pt

    return {"status": "created", "name": obj.name, "type": curve_type}


def create_text_object(params: dict) -> dict:
    name = params.get("name", "Text")
    text = params.get("text", "Hello")
    location = params.get("location", (0, 0, 0))
    size = params.get("size", 1.0)

    bpy.ops.object.text_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.body = text
    obj.data.size = size
    obj.data.extrude = params.get("extrude", 0.0)

    font_path = params.get("font_path")
    if font_path:
        obj.data.font = bpy.data.fonts.load(font_path)

    return {"status": "created", "name": obj.name, "text": text}


def edit_curve_points(params: dict) -> dict:
    curve_name = params["curve_name"]
    action = params.get("action", "add")
    obj = bpy.data.objects.get(curve_name)
    if not obj or obj.type != 'CURVE':
        return {"error": f"Curve '{curve_name}' not found"}

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    if action == "add":
        bpy.ops.curve.vertex_add()
    elif action == "remove":
        bpy.ops.curve.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    return {"status": f"curve_{action}"}


def set_curve_fill(params: dict) -> dict:
    obj = bpy.data.objects.get(params["curve_name"])
    if not obj or obj.type != 'CURVE':
        return {"error": f"Curve '{params['curve_name']}' not found"}
    obj.data.fill_mode = params.get("fill", "FULL")
    return {"status": "fill_set"}


def convert_curve_to_mesh(params: dict) -> dict:
    obj = bpy.data.objects.get(params["curve_name"])
    if not obj or obj.type != 'CURVE':
        return {"error": f"Curve '{params['curve_name']}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    return {"status": "converted_to_mesh", "name": obj.name}


HANDLERS = {
    "create_curve": create_curve,
    "create_text_object": create_text_object,
    "edit_curve_points": edit_curve_points,
    "set_curve_fill": set_curve_fill,
    "convert_curve_to_mesh": convert_curve_to_mesh,
}
