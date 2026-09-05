"""Render handlers — trigger renders, capture images."""

import bpy
import tempfile
import os
import base64


def render_image(params: dict) -> dict:
    output_path = params.get("output_path", "")
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), "blender_mcp_render.png")

    scene = bpy.context.scene
    if "resolution_x" in params:
        scene.render.resolution_x = params["resolution_x"]
    if "resolution_y" in params:
        scene.render.resolution_y = params["resolution_y"]
    if "samples" in params:
        engine = scene.render.engine
        if engine == 'CYCLES':
            scene.cycles.samples = params["samples"]
    if "engine" in params:
        scene.render.engine = params["engine"]

    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "rendered", "path": output_path, "image_base64": img_data[:200] + "..."}
    return {"status": "render_failed", "path": output_path}


def render_animation(params: dict) -> dict:
    output_path = params.get("output_path", "")
    if not output_path:
        output_path = os.path.join(tempfile.gettempdir(), "blender_mcp_anim")

    scene = bpy.context.scene
    scene.frame_start = params.get("frame_start", 1)
    scene.frame_end = params.get("frame_end", 250)
    if "engine" in params:
        scene.render.engine = params["engine"]
    scene.render.filepath = output_path
    bpy.ops.render.render(animation=True)
    return {"status": "animation_rendered", "path": output_path, "frames": f"{scene.frame_start}-{scene.frame_end}"}


def render_preview(params: dict) -> dict:
    quality = params.get("quality", "MEDIUM")
    sizes = {"LOW": (320, 240), "MEDIUM": (800, 600), "HIGH": (1920, 1080)}
    w, h = sizes.get(quality, (800, 600))

    scene = bpy.context.scene
    old_x, old_y = scene.render.resolution_x, scene.render.resolution_y
    old_engine = scene.render.engine
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_percentage = 100

    output_path = os.path.join(tempfile.gettempdir(), "blender_mcp_preview.png")
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

    scene.render.resolution_x = old_x
    scene.render.resolution_y = old_y
    scene.render.engine = old_engine

    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode("utf-8")
        return {"status": "preview_rendered", "path": output_path, "image_base64": img_data}
    return {"status": "preview_failed"}


HANDLERS = {
    "render_image": render_image,
    "render_animation": render_animation,
    "render_preview": render_preview,
}
