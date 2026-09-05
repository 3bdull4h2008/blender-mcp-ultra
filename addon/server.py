"""TCP socket server for Blender — accepts commands from MCP server, executes on main thread."""

import json
import queue
import socket
import struct
import threading
import time

import bpy

HEADER_FORMAT = "!I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
DEFAULT_PORT = 9876


class BlenderMCPServer:
    """Background TCP server that bridges the MCP server to Blender's main thread."""

    def __init__(self, host: str = "127.0.0.1", port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self._server_socket: socket.socket | None = None
        self._running = False
        self._thread: threading.Thread | None = None
        self._command_queue: queue.Queue = queue.Queue()
        self._response_queue: queue.Queue = queue.Queue()
        self._timer_registered = False

    def register(self):
        """Register the addon UI panel and start server."""
        bpy.utils.register_class(MCP_UL_StartServer)
        bpy.utils.register_class(MCP_PT_Panel)
        bpy.types.Scene.mcp_server_running = bpy.props.BoolProperty(default=False)
        bpy.types.Scene.mcp_server_port = bpy.props.IntProperty(
            name="Port", default=DEFAULT_PORT, min=1024, max=65535
        )
        self._start()

    def unregister(self):
        """Stop server and unregister UI."""
        self._stop()
        bpy.utils.unregister_class(MCP_UL_StartServer)
        bpy.utils.unregister_class(MCP_PT_Panel)
        del bpy.types.Scene.mcp_server_running
        del bpy.types.Scene.mcp_server_port

    def _start(self):
        if self._running:
            return
        self._running = True
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(1)
        self._server_socket.settimeout(1.0)

        self._thread = threading.Thread(target=self._server_loop, daemon=True)
        self._thread.start()

        if not self._timer_registered:
            bpy.app.timers.register(self._drain_queue, persistent=True, first_interval=0.05)
            self._timer_registered = True

        print(f"[Blender MCP Ultra] Server started on {self.host}:{self.port}")

    def _stop(self):
        self._running = False
        if self._server_socket:
            try:
                self._server_socket.close()
            except OSError:
                pass
            self._server_socket = None
        print("[Blender MCP Ultra] Server stopped")

    def _server_loop(self):
        while self._running:
            try:
                client, addr = self._server_socket.accept()
                client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                handler = threading.Thread(
                    target=self._handle_client, args=(client,), daemon=True
                )
                handler.start()
            except socket.timeout:
                continue
            except OSError:
                if self._running:
                    time.sleep(0.1)

    def _handle_client(self, client: socket.socket):
        try:
            while self._running:
                header = self._recv_exact(client, HEADER_SIZE)
                if not header:
                    break
                msg_len = struct.unpack(HEADER_FORMAT, header)[0]
                data = self._recv_exact(client, msg_len)
                if not data:
                    break

                command = json.loads(data.decode("utf-8"))

                self._command_queue.put((command, client))
                result = self._response_queue.get(timeout=180)

                resp_payload = json.dumps(result).encode("utf-8")
                resp_header = struct.pack(HEADER_FORMAT, len(resp_payload))
                client.sendall(resp_header + resp_payload)

        except (ConnectionResetError, BrokenPipeError, socket.timeout):
            pass
        except Exception as e:
            print(f"[Blender MCP Ultra] Client error: {e}")
        finally:
            client.close()

    def _drain_queue(self):
        """Process commands on Blender's main thread via timer."""
        while not self._command_queue.empty():
            try:
                command, client = self._command_queue.get_nowait()
            except queue.Empty:
                break

            try:
                result = self._execute_command(command)
            except Exception as e:
                result = {"error": str(e)}

            self._response_queue.put(result)

        return 0.01  # Re-run every 10ms

    def _execute_command(self, command: dict) -> dict:
        """Dispatch command to the appropriate handler."""
        from .handlers import DISPATCHER
        cmd_type = command.get("type", "")
        params = command.get("params", {})

        handler = DISPATCHER.get(cmd_type)
        if not handler:
            return {"error": f"Unknown command: {cmd_type}"}

        try:
            return handler(params)
        except Exception as e:
            return {"error": f"Handler error ({cmd_type}): {e}"}

    def _recv_exact(self, sock: socket.socket, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = sock.recv(n - len(data))
            if not chunk:
                return b""
            data += chunk
        return data


class MCP_UL_StartServer(bpy.types.Operator):
    """Start or stop the MCP server."""
    bl_idname = "mcp.toggle_server"
    bl_label = "Toggle MCP Server"

    def execute(self, context):
        scene = context.scene
        if scene.mcp_server_running:
            # Stop
            scene.mcp_server_running = False
            self.report({'INFO'}, "MCP Server stopped")
        else:
            scene.mcp_server_running = True
            self.report({'INFO'}, f"MCP Server started on port {scene.mcp_server_port}")
        return {'FINISHED'}


class MCP_PT_Panel(bpy.types.Panel):
    """MCP Ultra sidebar panel."""
    bl_label = "MCP Ultra"
    bl_idname = "MCP_PT_ultra_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MCP Ultra"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Server Status:")
        row.label(text="Running" if scene.mcp_server_running else "Stopped")

        row = layout.row()
        row.prop(scene, "mcp_server_port")

        row = layout.row()
        row.operator("mcp.toggle_server",
                      text="Stop Server" if scene.mcp_server_running else "Start Server")

        layout.separator()
        layout.label(text="Connect your MCP client to:")
        layout.label(text=f"127.0.0.1:{scene.mcp_server_port}")
