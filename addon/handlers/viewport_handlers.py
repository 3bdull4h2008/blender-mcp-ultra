"""Viewport handlers — screenshots, shading, overlays."""

import bpy
import bpy_extras
import tempfile
import os
import base64
import gpu
from gpu_extras.presets import draw_texture_2d


def get_viewport_screenshot(params: dict) -> dict:
    mode = params.get("mode", "fast")
    resolution = params.get("resolution", "MEDIUM")

    sizes = {"LOW": (320, 240), "MEDIUM": (800, 600), "HIGH": (1920, 1080), "ULTRA": (3840, 2160)}
    w, h = sizes.get(resolution, (800, 600))

    output_path = os.path.join(tempfile.gettempdir(), f"blender_mcp_screenshot_{w}x{h}.png")

    # Use OpenGL for fast capture
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            override['region'] = area.regions[-1]
            with bpy.context.temp_override(**override):
                bpy.ops.view3d.viewporter_render_to_image(filepath=output_path, resolution_percentage=100)
            break
    else:
        # Fallback: render viewport
        bpy.context.scene.render.filepath = output_path
        bpy.ops.render.render(write_still=True)

    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "screenshot_taken", "path": output_path, "image_base64": img_data}

    # If no viewport capture, render preview
    scene = bpy.context.scene
    old_engine = scene.render.engine
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    scene.render.engine = old_engine

    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "screenshot_rendered", "path": output_path, "image_base64": img_data}
    return {"status": "screenshot_failed"}


def get_render_preview(params: dict) -> dict:
    output_path = os.path.join(tempfile.gettempdir(), "blender_mcp_render_preview.png")
    scene = bpy.context.scene
    old_engine = scene.render.engine
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    scene.render.engine = old_engine
    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "preview", "image_base64": img_data}
    return {"status": "preview_failed"}


def get_viewport_info(params: dict) -> dict:
    scene = bpy.context.scene
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            return {
                "shading": space.shading.type,
                "camera": scene.camera.name if scene.camera else None,
                "cursor_location": list(scene.cursor.location),
                "overlay": space.overlay.show_overlays,
            }
    return {"status": "no_3d_viewport"}


def set_viewport_shading(params: dict) -> dict:
    mode = params.get("mode", "SOLID")
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.shading.type = mode
            return {"status": "shading_set", "mode": mode}
    return {"error": "No 3D viewport found"}


def set_viewport_camera(params: dict) -> dict:
    cam_name = params.get("camera_name", "")
    if cam_name:
        cam = bpy.data.objects.get(cam_name)
        if cam:
            bpy.context.scene.camera = cam
    return {"status": "viewport_camera_set"}


def toggle_overlays(params: dict) -> dict:
    show = params.get("show", True)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.overlay.show_overlays = show
            return {"status": "overlays_toggled", "show": show}
    return {"error": "No 3D viewport found"}


HANDLERS = {
    "get_viewport_screenshot": get_viewport_screenshot,
    "get_render_preview": get_render_preview,
    "get_viewport_info": get_viewport_info,
    "set_viewport_shading": set_viewport_shading,
    "set_viewport_camera": set_viewport_camera,
    "toggle_overlays": toggle_overlays,
    "take_screenshot": get_viewport_screenshot,
}
