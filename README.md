# Blender MCP Ultra

**The ultimate Blender MCP server** — 150+ tools, expert prompts, visual feedback, mesh quality analysis, and goal-first routing. Better than paid alternatives.

## What This Is

A production-grade [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that gives AI agents complete control of Blender. It combines the best features from all existing Blender MCP projects into a single, modular, well-tested package.

## Features

- **150+ structured tools** across 24 modules (scene, objects, transforms, modeling, mesh editing, materials, lighting, camera, animation, rendering, viewport, sculpting, UV, physics, geometry nodes, curves, armature, collections, file I/O, procedural generation, code execution)
- **12 expert prompts** — topology best practices, real-world scale references, lighting principles, PBR material recipes, character basemesh workflow, product shot setup, auto-critique workflow, undo strategy, animation principles, scene cleanup, render style presets, common operators reference
- **Visual feedback loop** — fast viewport screenshots via OpenGL with auto-critique prompts that guide the LLM to check its own work
- **Mesh quality analysis** — non-manifold edges, loose vertices, zero-area faces, duplicate vertices, production readiness score
- **Goal-first session management** — structured workflow phases (plan → build → inspect → finish)
- **Thread-safe architecture** — background TCP server with queue-based main-thread execution
- **Zero telemetry** — everything runs locally on 127.0.0.1
- **Blender 4.2+ compatible** — ships as a Blender Extension
- **Modular addon** — 21 handler modules, each covering a specific Blender domain
- **Comprehensive validation** — all inputs sanitized before reaching Blender

## Architecture

```
AI Agent ←stdio/MCP→ blender-mcp-ultra server ←TCP socket→ Blender addon ←bpy→ Blender
```

### MCP Server (`src/blender_mcp_ultra/`)
- FastMCP server with tools, prompts, and resources
- TCP client with length-prefixed JSON protocol
- Input validation and security sandboxing
- Session management with goal tracking

### Blender Addon (`addon/`)
- Background TCP socket server on 127.0.0.1:9876
- Command queue drained on Blender's main thread via `bpy.app.timers`
- 21 handler modules for each Blender domain
- N-panel UI for start/stop and port configuration
- Zero external dependencies — uses only Python stdlib + `bpy`

## Quick Start

### 1. Install the MCP Server

```bash
cd "blender-mcp-ultra"
pip install -e .
# or
uv pip install -e .
```

### 2. Install the Blender Addon

1. Open Blender 4.2+
2. Go to **Edit > Preferences > Get Extensions**
3. Click **Install from Disk**
4. Select the `addon/` directory from this project
5. Enable "Blender MCP Ultra" in the extensions list
6. Click **Start MCP Server** in the N-panel (View3D > Sidebar > MCP Ultra)

### 3. Connect Your MCP Client

Add to your MCP client config:

```json
{
  "mcpServers": {
    "blender": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/blender-mcp-ultra", "blender-mcp-ultra"]
    }
  }
}
```

## Tool Modules (24)

| Module | Tools | Description |
|--------|-------|-------------|
| Scene | 8 | Scene info, create/delete, render settings |
| Objects | 11 | Create, delete, duplicate, parent, join |
| Transforms | 8 | Move, rotate, scale, align, snap |
| Modeling | 14 | Modifiers, booleans, extrude, bevel, subdivision |
| Mesh Editing | 10 | Vertex/edge/face operations, vertex groups |
| Mesh Quality | 7 | Defect analysis, production readiness |
| Materials | 10 | Create, assign, procedural materials, shader nodes |
| Lighting | 7 | Lights, three-point, HDRI, studio presets |
| Camera | 5 | Create, configure, turntable, track-to |
| Animation | 8 | Keyframes, interpolation, walk cycles |
| Rendering | 3 | Render image/animation/preview |
| Viewport | 7 | Screenshots, shading, overlays |
| Sculpting | 6 | Brush config, sculpt mode, dyntopo, remesh |
| UV | 6 | Smart project, unwrap, pack, info |
| Physics | 7 | Rigid body, cloth, fluid, particles, force fields |
| Geometry Nodes | 4 | Modifiers, nodes, procedural distribution |
| Curves | 5 | Bezier, text, edit, convert |
| Armature | 6 | Bones, humanoid rig, IK chain |
| Collections | 5 | Create, delete, move, visibility |
| File I/O | 5 | Import/export FBX, OBJ, GLTF, STL, USD |
| Procedural | 4 | Terrain, tree, rock, particle field |
| Code Exec | 3 | Execute Python, scripts, operators |

## Expert Prompts (12)

1. **Topology Best Practices** — quad topology, edge flow, n-gon cleanup
2. **Scale Reference Guide** — real-world dimensions for characters, architecture, props
3. **Lighting Principles** — three-point lighting, color temperature, EEVEE vs Cycles
4. **Material Workflow Guide** — PBR recipes, texture color spaces
5. **Auto-Critique Workflow** — visual feedback loop for self-assessment
6. **Character Basemesh Workflow** — step-by-step character creation
7. **Product Shot Setup** — professional product photography
8. **Animation Principles** — 12 principles applied to Blender
9. **Scene Cleanup** — naming conventions, organization, optimization
10. **Render Style Presets** — photorealistic, toon, product, archviz, pixel art
11. **Undo Strategy** — managing undo/redo in AI workflows
12. **Workflow Orchestration** — multi-step 3D workflow planning

## What Makes This Better Than Paid Alternatives

| Feature | Blender MCP Ultra | Paid Tools |
|---------|-------------------|------------|
| Tool count | 150+ | 20-50 |
| Expert prompts | 12 | 0-3 |
| Mesh quality analysis | Full | Basic |
| Visual feedback loop | Yes | Limited |
| Goal-first routing | Yes | No |
| Session management | Stateful | Stateless |
| Open source | MIT | Proprietary |
| Telemetry | Zero | Often included |
| Customizable | Full | Limited |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check src/

# Run tests
pytest tests/
```

## License

MIT — do whatever you want with it.

## Credits

Built by analyzing and combining the best ideas from:
- [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) — the original
- [HoldMyBeer-gg/blend-ai](https://github.com/HoldMyBeer-gg/blend-ai) — 164 tools, expert prompts
- [PatrykIti/blender-ai-mcp](https://github.com/PatrykIti/blender-ai-mcp) — goal-first routing
