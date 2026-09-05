"""MCP Prompts — expert guidance for AI agents on 3D workflows."""

from blender_mcp_ultra.server import mcp


@mcp.prompt()
def topology_best_practices() -> str:
    """Expert guide to mesh topology for clean, production-ready geometry."""
    return """TOPOLOGY BEST PRACTICES FOR BLENDER MESHES:

1. QUAD-BASED TOPOLOGY
   - Prefer quads over tris and ngons for subdivision compatibility
   - Use 4-sided faces that follow the form's curvature
   - Avoid poles (vertices with 5+ connected edges) in smooth areas
   - Limit poles to flat areas or sharp corners

2. EDGE FLOW
   - Edges should follow the natural contour of the shape
   - Add edge loops where form changes direction
   - Use supporting edge loops near sharp edges for subdivision
   - Maintain consistent edge density — avoid stretching

3. N-GON CLEANUP
   - Convert ngons to quads/tris before subdivision
   - Use Grid Fill or Patch Fill for complex holes
   - For hard surfaces: boolean → dissolve → manual cleanup

4. FACE DENSITY
   - Keep face sizes relatively uniform across the mesh
   - Increase density only where detail is needed
   - Use Multi-Resolution or subdivision for level-of-detail

5. MODIFIER WORKFLOW
   - Model in low-poly, add detail with modifiers
   - Mirror modifier for symmetry (apply only when done)
   - Solidify for thin surfaces, Subdivision for smooth curves
   - Boolean last, then clean up topology"""


@mcp.prompt()
def scale_reference_guide() -> str:
    """Real-world scale references for accurate 3D modeling."""
    return """REAL-WORLD SCALE REFERENCES (meters):

CHARACTERS:
  Human (average)    1.75m tall, 0.45m shoulder width
  Child (5yr)        1.10m tall
  Dwarf              1.30m tall
  Giant              2.50m+ tall

ARCHITECTURE:
  Door height        2.10m
  Door width         0.90m
  Ceiling height     2.70m (residential), 3.50m+ (commercial)
  Stair rise         0.18m per step
  Stair run          0.28m per step
  Countertop height  0.90m
  Table height       0.75m
  Chair seat height  0.45m

VEHICLES:
  Car length         4.50m
  Car width          1.80m
  Car height         1.50m
  Truck length       8-16m
  Bicycle length     1.70m

PROPS:
  Coffee cup         0.09m tall, 0.08m diameter
  Book               0.23m × 0.15m × 0.03m
  Smartphone         0.15m × 0.07m × 0.008m
  Basketball         0.24m diameter
  Soccer ball        0.22m diameter
  Baseball bat       1.07m long

ENVIRONMENT:
  Tree height        10-30m (varies by type)
  Grass blade        0.05-0.15m
  Rock (small)       0.1-0.3m
  Rock (large)       1-5m
  River width        5-50m
  Mountain           1000-5000m

TIP: Always check Object > Properties > Dimensions against these references.
Model at real scale for correct lighting, physics, and rendering behavior."""


@mcp.prompt()
def lighting_principles() -> str:
    """Professional lighting principles for 3D scenes."""
    return """LIGHTING PRINCIPLES FOR BLENDER:

THREE-POINT LIGHTING (Foundation):
  Key Light:   Main source, 45° to side, 45° above. Energy: 1000W.
  Fill Light:  Opposite side, softer. Energy: 1/3 of key (~300W).
  Rim Light:   Behind subject, creates edge separation. Energy: 1/2 of key (~500W).

COLOR TEMPERATURE:
  Warm (tungsten):  3200K — orange/yellow, cozy interiors
  Daylight:         5500K — neutral white, outdoor scenes
  Cool (shade):     7500K — blue tint, overcast skies
  Neon:             8000K+ — vibrant, sci-fi

SHADOW SOFTNESS:
  Hard shadows:    Small light source, close to subject
  Soft shadows:    Large light source, far from subject
  Use Area lights for natural soft shadows
  Sun lights = infinite distance = hard shadows always

EEVEE vs CYCLES:
  EEVEE:   Faster, screen-space effects, good for real-time
  Cycles:  Path-traced, physically accurate, better shadows/reflections
  For product/archviz: use Cycles with 256+ samples
  For animation: EEVEE with baked lightmaps or probe-based GI

HDRI LIGHTING:
  - Use for realistic environmental reflections
  - Control strength to balance with artificial lights
  - Rotate for different shadow directions
  - Best for product shots and outdoor scenes

COMMON MISTAKES:
  - Using only one light (flat, boring)
  - Too many lights (washed out, no depth)
  - Lights too bright/overexposed
  - No rim light (subject blends into background)
  - Ignoring light color (everything is white)"""


@mcp.prompt()
def material_workflow_guide() -> str:
    """PBR material creation guide with real-world recipes."""
    return """PBR MATERIAL WORKFLOW GUIDE:

PRINCIPLED BSDF INPUTS:
  Base Color:    Albedo/diffuse color (sRGB)
  Metallic:      0 = dielectric, 1 = metal. No in-between for realism.
  Roughness:     0 = mirror, 1 = matte. Most materials 0.2-0.8
  Specular:      0.5 default. 0.3-0.4 for low-reflectance materials
  Normal:        Normal map for surface detail
  Emission:      Self-illumination color

MATERIAL RECIPES:

  POLISHED METAL (chrome, steel):
    Metallic: 1.0, Roughness: 0.05-0.15, Base Color: gray

  BRUSHED METAL:
    Metallic: 1.0, Roughness: 0.3-0.5, Base Color: gray
    Add anisotropic texture to roughness

  WOOD:
    Metallic: 0.0, Roughness: 0.6-0.8
    Use procedural noise + color ramp for grain
    Dark: walnut/oak, Light: birch/pine

  GLASS:
    Metallic: 0.0, Roughness: 0.0, Alpha: 0.0-0.1
    Transmission: 1.0, IOR: 1.45-1.52
    Use Alpha Blend or Hashed for EEVEE

  PLASTIC (shiny):
    Metallic: 0.0, Roughness: 0.15-0.3
    Base Color: vibrant color, Specular: 0.5

  CONCRETE:
    Metallic: 0.0, Roughness: 0.8-0.95
    Base Color: light gray with subtle variation

  FABRIC/CLOTH:
    Metallic: 0.0, Roughness: 0.7-0.95
    Use sheen for velvet/silk effects
    Subsurface for thin fabrics

  SKIN:
    Metallic: 0.0, Roughness: 0.4-0.6
    Subsurface: 0.1-0.5 with red/orange tint
    Subsurface Radius: [1.0, 0.2, 0.1]

TEXTURE COLOR SPACES:
  Base Color: sRGB
  Normal: Non-Color
  Roughness: Non-Color
  Metallic: Non-Color
  Ambient Occlusion: Non-Color"""


@mcp.prompt()
def auto_critique_workflow() -> str:
    """Visual feedback loop guide for AI self-assessment."""
    return """AUTO-CRITIQUE WORKFLOW:

After making significant changes to a 3D scene, ALWAYS:

1. SCREENSHOT the viewport (use get_viewport_screenshot with mode='fast')
2. ASSESS the result against these criteria:
   - Form: Does the shape match the intent?
   - Scale: Are proportions realistic?
   - Materials: Do materials look believable?
   - Lighting: Is the scene well-lit with clear hierarchy?
   - Composition: Is the arrangement visually pleasing?

3. CHECK MESH QUALITY:
   - Call analyze_mesh_quality for defect reports
   - Fix non-manifold edges, loose vertices, zero-area faces
   - Verify manifold status before finalizing

4. ITERATE if needed:
   - Make targeted corrections
   - Screenshot again
   - Compare before/after

TOKEN BUDGET RULES:
   - Keep critique responses under 200 tokens
   - Focus on the most critical issues first
   - Don't repeat the same observation twice
   - Track what's been fixed vs. what remains

WHEN TO SCREENSHOT:
   - After creating or significantly modifying geometry
   - After applying materials
   - After changing lighting setup
   - Before considering the task complete
   - When the user asks to "check" or "verify"

WHEN NOT TO SCREENSHOT:
   - After minor parameter tweaks
   - During multi-step sequential operations (batch first, screenshot at end)
   - When the user explicitly says not to"""


@mcp.prompt()
def character_basemesh_workflow() -> str:
    """Step-by-step guide for creating character base meshes."""
    return """CHARACTER BASE MESH WORKFLOW:

STEP 1: CUBE START
  - Create a cube (2m × 2m × 2m for human scale)
  - Add Mirror modifier (clipping on)
  - Add Subdivision Surface (levels 2 viewport, 3 render)

STEP 2: BODY PROPORTIONS
  - Scale cube to body proportions (1 head = 0.25m)
  - 7.5 heads tall for adults
  - Extrude for torso, arms, legs
  - Use loop cuts for joints (shoulders, elbows, knees)

STEP 3: HEAD & FACE
  - Extrude from top of torso
  - Side loops for eyes, mouth
  - Nose, ears as separate geometry or extruded
  - Keep very low-poly at this stage

STEP 4: HANDS & FEET
  - Extrude from wrist/ankle
  - 5 fingers: start with mitt, then separate
  - Foot: simple wedge shape

STEP 5: TOPOLOGY CHECK
  - All quads, no ngons at joints
  - Edge loops follow muscle groups
  - Symmetry maintained via mirror

STEP 6: DETAIL PASS
  - Add edge loops for definition
  - Sculpt mode for organic details
  - Retopologize if needed for game/animation

IMPORTANT PRINCIPLES:
  - Start simple, add complexity gradually
  - Model at real scale (1.75m for average human)
  - Keep symmetry until final
  - Test deformations early (add armature, bend joints)
  - Low poly = easier to edit, subdivision adds smoothness"""


@mcp.prompt()
def product_shot_setup() -> str:
    """Professional product photography setup guide."""
    return """PRODUCT SHOT SETUP IN BLENDER:

SCENE SETUP:
  1. Create backdrop (large curved plane or cyclorama)
  2. Place product at world origin
  3. Set camera at eye level or slightly above

LIGHTING (3-point for products):
  Key:    Area light, 45° right, 45° above, 1000W
  Fill:   Area light, left side, 300W, slightly behind
  Rim:    Point light behind product, 500W
  Bonus:  Add a soft box (large area light) above for even illumination

CAMERA:
  - Lens: 85-135mm (product), 50mm (lifestyle)
  - F-stop: f/8-f/11 for sharp product
  - Depth of field: ON, focus on product center
  - Clip start: 0.1m

MATERIALS:
  - Use Cycles for accurate reflections
  - Set world environment to neutral gray or HDRI
  - Enable color management (Filmic or AgX)

RENDER SETTINGS:
  - Engine: Cycles
  - Samples: 256-512
  - Denoising: ON
  - Resolution: 2000×2000 for product, 1920×1080 for lifestyle

COMPOSITION:
  - Rule of thirds for product placement
  - Leave negative space for text/logos
  - Multiple angles: front, 3/4, side, detail, overhead
  - Use depth of field to separate from background

POST-PROCESSING:
  - Compositor: glare for highlights
  - Color balance for mood
  - Vignette for focus"""


@mcp.prompt()
def animation_principles() -> str:
    """12 principles of animation applied to Blender 3D."""
    return """12 PRINCIPLES OF ANIMATION IN BLENDER:

1. SQUASH & STRETCH
   - Add shape keys or use lattice for deformation
   - Exaggerate for cartoon, subtle for realistic
   - Keep volume constant

2. ANTICIPATION
   - Wind-up before the main action
   - Reverse direction briefly before forward motion
   - Set keyframes 5-10 frames before action start

3. STAGING
   - Direct attention with lighting, camera, and posing
   - One clear idea per pose
   - Use silhouette test (pose must read in shadow)

4. STRAIGHT AHEAD & POSE-TO-POSE
   - Pose-to-pose: key poses first, then in-betweens
   - Straight ahead: frame-by-frame for organic motion
   - Combine both for best results

5. FOLLOW THROUGH & OVERLAPPING ACTION
   - Different parts stop at different times
   - Hair/clothes continue after body stops
   - Use secondary motion modifiers

6. SLOW IN & SLOW OUT
   - Ease keyframes (Bezier interpolation)
   - More keyframes at start/end of motion
   - Use graph editor to fine-tune curves

7. ARCS
   - Natural motion follows curved paths
   - Adjust motion paths in graph editor
   - Circular motion for limbs

8. SECONDARY ACTION
   - Supporting motions that complement the main action
   - Example: character talks (primary) + gestures (secondary)

9. TIMING
   - Frame count = speed of action
   - 24 fps standard, 30/60 for smooth motion
   - Fast: 3-6 frames, Slow: 12-24 frames

10. EXAGGERATION
    - Push poses beyond reality for appeal
    - 20-50% more than real life
    - Essential for animation personality

11. SOLID DRAWING (Posing)
    - Strong silhouettes
    - Weight and balance
    - Use reference for complex poses

12. APPEAL
    - Characters should be interesting to watch
    - Clear design, readable poses
    - Avoid uncanny valley"""


@mcp.prompt()
def scene_cleanup_workflow() -> str:
    """Scene organization and cleanup checklist."""
    return """SCENE CLEANUP WORKFLOW:

NAMING CONVENTIONS:
  - Objects: descriptive_name (e.g., "building_01", "tree_oak_03")
  - Materials: descriptive_mat (e.g., "wood_dark_mat")
  - Collections: Category_Group (e.g., "Environment_Trees")
  - Avoid: Cube.001, Material.003 (auto-generated names)

ORGANIZATION:
  1. Sort objects into logical collections (Environment, Characters, Props, Lights)
  2. Use prefixes/suffixes for types: _COL, _LGT, _CAM
  3. Hide inactive collections in viewport
  4. Lock transform on static objects

CLEANUP STEPS:
  1. File > Clean Up > Unused Data-Blocks (remove orphans)
  2. File > Clean Up > Recursive Unused Data-Blocks
  3. Remove hidden/unused objects
  4. Apply all modifiers that are finalized
  5. Merge duplicate materials
  6. Check for orphaned vertex groups
  7. Remove empty vertex groups from objects

OPTIMIZATION:
  1. Decimate high-poly objects not in close-up
  2. Use instancing for repeated objects
  3. Bake textures for complex materials
  4. Apply modifiers before export
  5. Check polygon count per object

BEFORE EXPORT:
  1. Apply all transforms (Ctrl+A > All Transforms)
  2. Check normals are consistent
  3. Verify UV mapping is correct
  4. Test in target application
  5. Save a backup before export"""


@mcp.prompt()
def render_style_presets() -> str:
    """Rendering style presets for different use cases."""
    return """RENDER STYLE PRESETS:

PHOTOREALISTIC:
  Engine: Cycles, Samples: 512-1024
  Denoising: OpenImageDenoise
  Color Management: AgX or Filmic
  Light Path: Max Bounces 8-12
  Use HDRI + 3-point lighting
  Material: full PBR with roughness/metallic maps

STYLIZED/TOON:
  Engine: EEVEE or Grease Pencil
  Use Shader to RGB node for toon shading
  Flat colors with hard shadows
  Outline via Solidify modifier (inverted normals)
  No subsurface scattering

PRODUCT/STUDIO:
  Engine: Cycles, Samples: 256
  Clean backdrop (white/gray cyclorama)
  Even, soft lighting (large area lights)
  Camera: 85mm, f/8, DOF on product
  Post: glare, color balance

ARCHITECTURAL:
  Engine: Cycles, Samples: 256-512
  HDRI for environment + sunlight
  Use Light Path > Glossy bounces: 4
  Interior: many small lights, low intensity
  Exterior: sun + sky texture

PIXEL ART:
  Render at target resolution (e.g., 320×240)
  Scale up with nearest-neighbor interpolation
  Limit colors to palette
  Use flat shading, no smooth
  EEVEE, 1 sample, no anti-aliasing

ANIMATION PREVIEW:
  Engine: EEVEE
  Samples: 32-64 (fast)
  Resolution: 50-75% of final
  Disable motion blur
  Viewport render for timing check

HIGH-QUALITY STILL:
  Engine: Cycles
  Samples: 1024-4096
  Denoising: ON
  Resolution: 4K (3840×2160)
  Render border for test crops first"""


@mcp.prompt()
def undo_strategy() -> str:
    """Guide for managing undo/redo in AI-driven Blender workflows."""
    return """UNDO STRATEGY FOR AI AGENTS:

BLENDER UNDO SYSTEM:
  - Ctrl+Z: undo last operation
  - Ctrl+Shift+Z: redo
  - Undo stack: limited (default 32 steps)
  - Each bpy.ops call = one undo step

AI AGENT UNDO BEST PRACTICES:

1. CHECKPOINT BEFORE DESTRUCTIVE OPERATIONS
   - Save file before major changes: bpy.ops.wm.save_as_mainfile()
   - Note the current state in your response
   - "Saved checkpoint before boolean operation"

2. GROUP RELATED OPERATIONS
   - Use execute_blender_code for multi-step sequences
   - One code block = one undo step
   - Better than 5 separate tool calls

3. VERIFY BEFORE COMMITTING
   - Screenshot before and after
   - Check mesh quality before complex operations
   - "I'll verify the result before proceeding"

4. RECOVERY PATTERNS
   - Undo multiple steps: bpy.ops.ed.undo() in a loop
   - Reset to saved: bpy.ops.wm.open_mainfile()
   - Object-level undo: delete and re-create

5. COMMON MISTAKES TO UNDO
   - Accidental scale in wrong space
   - Boolean operation with wrong object
   - Material assigned to wrong slot
   - Modifiers applied prematurely

6. COMMUNICATION
   - Tell the user when you're about to do something risky
   - "This operation is destructive. I recommend saving first."
   - Offer undo instructions: "Press Ctrl+Z to undo this step"

7. AUTO-UNDO SUPPORT
   - The addon can auto-push undo steps
   - Configurable per-operation type
   - Read-only operations don't push undo"""


@mcp.prompt()
def workflow_orchestration() -> str:
    """Best practices for multi-step 3D workflows."""
    return """WORKFLOW ORCHESTRATION GUIDE:

PLANNING PHASE:
  1. Understand the goal completely before starting
  2. Break down into clear steps
  3. Identify dependencies between steps
  4. Choose the right tools for each step
  5. Estimate complexity and time

EXECUTION PHASE:
  1. Start with broad strokes (basic shapes)
  2. Add detail progressively
  3. Verify at each major milestone
  4. Fix issues before building on top
  5. Keep the scene organized throughout

COMMON WORKFLOWS:

  PRODUCT MODELING:
    1. Reference images → block out → refine → detail → material → render

  ENVIRONMENT:
    1. Terrain → large structures → medium props → small details → lighting → atmosphere

  CHARACTER:
    1. Base mesh → proportions → anatomy → details → rig → weight paint → animate

  ARCHVIZ:
    1. Floor plan → walls → windows/doors → furniture → materials → lighting → render

QUALITY CHECKPOINTS:
  - After modeling: check topology, normals, scale
  - After materials: check UV mapping, texture resolution
  - After lighting: check shadows, exposure, color balance
  - Before render: check render settings, denoising, output path

ERROR RECOVERY:
  - If something looks wrong, screenshot and analyze
  - Don't keep building on a broken foundation
  - Undo to the last known-good state
  - Try a different approach

COMMUNICATION:
  - Explain your plan before executing
  - Show progress at milestones
  - Ask for feedback on subjective choices
  - Report completion with screenshots"""


@mcp.prompt()
def common_operator_reference() -> str:
    """Quick reference for commonly used Blender operators."""
    return """COMMON BLENDER OPERATORS QUICK REFERENCE:

MESH PRIMITIVES:
  mesh.primitive_cube_add(size=2, location=(0,0,0))
  mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16)
  mesh.primitive_cylinder_add(radius=1, depth=2, vertices=32)
  mesh.primitive_cone_add(radius1=1, radius2=0, depth=2)
  mesh.primitive_torus_add(major_radius=1, minor_radius=0.25)
  mesh.primitive_plane_add(size=2)
  mesh.primitive_ico_sphere_add(radius=1, subdivisions=2)

MESH OPERATIONS:
  mesh.extrude_region_move()
  mesh.inset_faces(thickness=0.1)
  mesh.bevel(offset=0.1, segments=1)
  mesh.subdivide(number_cuts=1)
  mesh.remove_doubles(threshold=0.001)
  mesh.normals_make_consistent(inside=False)
  mesh.select_all(action='SELECT')
  mesh.select_all(action='DESELECT')
  mesh.select_more()
  mesh.select_less()

OBJECT OPERATIONS:
  object.location_set(location=(0,0,0))
  object.rotation_set(rotation=(0,0,0))
  object.scale_set(scale=(1,1,1))
  object.origin_set(type='ORIGIN_GEOMETRY')
  object.shade_smooth()
  object.shade_flat()
  object.delete(use_global=False)

TRANSFORM:
  transform.translate(value=(0,0,0))
  transform.rotate(value=0, axis=(0,0,1))
  transform.resize(value=(1,1,1))
  transform.apply(location=False, rotation=False, scale=True)

MODIFIER:
  modifier.add(type='SUBSURF', name='Subdivision')
  modifier.add(type='MIRROR', name='Mirror')
  modifier.add(type='SOLIDIFY', name='Solidify')
  modifier.add(type='BOOLEAN', name='Boolean')
  modifier.add(type='BEVEL', name='Bevel')
  modifier.add(type='ARRAY', name='Array')
  modifier.apply(modifier='ModifierName')

EDIT MODE:
  bpy.ops.object.mode_set(mode='EDIT')
  bpy.ops.mesh.select_mode(type='VERT')
  bpy.ops.mesh.select_mode(type='EDGE')
  bpy.ops.mesh.select_mode(type='FACE')
  bpy.ops.object.mode_set(mode='OBJECT')"""
