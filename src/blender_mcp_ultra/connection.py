"""TCP connection to the Blender addon — length-prefixed JSON protocol."""

import json
import logging
import socket
import struct
import threading
import time
from typing import Any

logger = logging.getLogger("blender_mcp_ultra.connection")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9876
MAX_RETRIES = 3
RETRY_DELAY = 2.0
SEND_TIMEOUT = 180.0
HEADER_FORMAT = "!I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


class BlenderConnection:
    """Thread-safe TCP client for communicating with the Blender addon."""

    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        self.host = host
        self.port = port
        self._socket: socket.socket | None = None
        self._lock = threading.Lock()
        self._connected = False
        self._render_busy = False

    @property
    def connected(self) -> bool:
        return self._connected and self._socket is not None

    def connect(self) -> bool:
        """Establish TCP connection to Blender addon."""
        for attempt in range(MAX_RETRIES):
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self._socket.settimeout(10.0)
                self._socket.connect((self.host, self.port))
                self._connected = True
                self._socket.settimeout(None)
                logger.info("Connected to Blender addon at %s:%d", self.host, self.port)
                return True
            except (ConnectionRefusedError, OSError) as e:
                logger.warning("Connection attempt %d/%d failed: %s", attempt + 1, MAX_RETRIES, e)
                if self._socket:
                    self._socket.close()
                    self._socket = None
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        self._connected = False
        return False

    def disconnect(self):
        """Close the TCP connection."""
        with self._lock:
            self._connected = False
            if self._socket:
                try:
                    self._socket.close()
                except OSError:
                    pass
                self._socket = None
        logger.info("Disconnected from Blender addon")

    def send_command(self, command_type: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a command to Blender and return the response.

        Args:
            command_type: The command identifier (e.g. 'get_scene_info').
            params: Command parameters.

        Returns:
            The response dictionary from Blender.

        Raises:
            ConnectionError: If not connected.
            TimeoutError: If Blender does not respond within timeout.
            RuntimeError: If Blender reports an error.
        """
        if not self.connected:
            if not self.connect():
                raise ConnectionError(
                    "Cannot connect to Blender addon. "
                    "Make sure Blender is running with the blender-mcp-ultra addon enabled."
                )

        with self._lock:
            payload = json.dumps({"type": command_type, "params": params or {}}).encode("utf-8")
            header = struct.pack(HEADER_FORMAT, len(payload))

            try:
                self._socket.sendall(header + payload)
            except OSError as e:
                self._connected = False
                raise ConnectionError(f"Failed to send command: {e}") from e

            try:
                self._socket.settimeout(SEND_TIMEOUT)
                resp_header = self._recv_exact(HEADER_SIZE)
                resp_len = struct.unpack(HEADER_FORMAT, resp_header)[0]
                resp_data = self._recv_exact(resp_len)
            except socket.timeout:
                self._connected = False
                raise TimeoutError(
                    f"Blender did not respond within {SEND_TIMEOUT}s. "
                    "The operation may be too long or Blender may be frozen."
                )
            except OSError as e:
                self._connected = False
                raise ConnectionError(f"Failed to receive response: {e}") from e
            except (AttributeError, TypeError):
                raise ConnectionError("Connection was closed")
            finally:
                try:
                    if self._socket:
                        self._socket.settimeout(None)
                except (AttributeError, OSError):
                    pass

            response = json.loads(resp_data.decode("utf-8"))

            if response.get("render_busy"):
                self._render_busy = True
            else:
                self._render_busy = False

            if "error" in response:
                raise RuntimeError(response["error"])

            return response

    def _recv_exact(self, n: int) -> bytes:
        """Receive exactly n bytes from the socket."""
        data = b""
        while len(data) < n:
            if not self._socket:
                raise ConnectionError("Connection closed")
            chunk = self._socket.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed by Blender addon")
            data += chunk
        return data

    def is_render_busy(self) -> bool:
        """Check if Blender is currently rendering."""
        return self._render_busy


_connection: BlenderConnection | None = None
_connection_lock = threading.Lock()


def get_blender_connection(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> BlenderConnection:
    """Get or create the singleton Blender connection."""
    global _connection
    with _connection_lock:
        if _connection is None or not _connection.connected:
            _connection = BlenderConnection(host, port)
        return _connection
