"""Input validation and sanitization for all MCP tool parameters."""

import os
import re
from pathlib import PurePosixPath


class Validator:
    """Validates and sanitizes tool inputs before forwarding to Blender."""

    NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.\s]+$")
    SAFE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]+$")
    MAX_NAME_LENGTH = 256
    MAX_CODE_LENGTH = 100_000

    DANGEROUS_IMPORTS = frozenset([
        "os", "sys", "subprocess", "shutil", "socket", "http", "urllib",
        "requests", "ctypes", "importlib", "pathlib", "glob", "pickle",
        "marshal", "shelve", "sqlite3", "mysql", "psycopg", "asyncio",
        "threading", "multiprocessing", "signal", "ctypes", "code",
        "codeop", "compileall", "webbrowser", "antigravity", "turtle",
        "tkinter", "smtplib", "xmlrpc", "ftplib", "telnetlib", "uuid",
    ])

    DANGEROUS_BUILTINS = frozenset([
        "__import__", "exec", "eval", "compile", "open", "globals",
        "locals", "vars", "input", "breakpoint", "exit", "quit",
        "help", "memoryview", "credits", "license", "copyright",
    ])

    ENUMS = {
        "object_type": {"MESH", "CURVE", "SURFACE", "META", "TEXT", "ARMATURE",
                        "LATTICE", "EMPTY", "CAMERA", "LIGHT", "SPEAKER",
                        "FORCE_FIELD", "GPENCIL", "COLLECTION"},
        "light_type": {"POINT", "SUN", "SPOT", "AREA"},
        "blend_mode": {"OPAQUE", "CLIP", "HASHED", "BLEND"},
        "transform_space": {"WORLD", "LOCAL"},
        "shading": {"FLAT", "SMOOTH"},
        "bool_operation": {"UNION", "INTERSECT", "DIFFERENCE"},
        "render_engine": {"BLENDER_EEVEE", "CYCLES", "BLENDER_WORKBENCH"},
        "axis": {"X", "Y", "Z", "-X", "-Y", "-Z"},
    }

    @classmethod
    def validate_name(cls, name: str, allow_spaces: bool = False) -> str:
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        name = name.strip()[:cls.MAX_NAME_LENGTH]
        pattern = cls.NAME_PATTERN if allow_spaces else cls.SAFE_NAME_PATTERN
        if not pattern.match(name):
            raise ValueError(f"Invalid name: {name!r}")
        return name

    @classmethod
    def validate_float(cls, value: float, min_val: float = -1e6, max_val: float = 1e6) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid float value: {value!r}")
        if not (-1e10 < v < 1e10):
            raise ValueError(f"Value out of range: {v}")
        return max(min_val, min(max_val, v))

    @classmethod
    def validate_int(cls, value: int, min_val: int = -100000, max_val: int = 100000) -> int:
        try:
            v = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid integer value: {value!r}")
        return max(min_val, min(max_val, v))

    @classmethod
    def validate_color(cls, color: list) -> list[float]:
        if not isinstance(color, (list, tuple)) or len(color) not in (3, 4):
            raise ValueError("Color must be [R, G, B] or [R, G, B, A]")
        return [max(0.0, min(1.0, float(c))) for c in color]

    @classmethod
    def validate_vector(cls, vec: list, length: int = 3) -> list[float]:
        if not isinstance(vec, (list, tuple)) or len(vec) != length:
            raise ValueError(f"Vector must have {length} components")
        return [float(v) for v in vec]

    @classmethod
    def validate_enum(cls, value: str, enum_name: str) -> str:
        allowed = cls.ENUMS.get(enum_name)
        if allowed and value.upper() not in allowed:
            raise ValueError(f"Invalid {enum_name}: {value!r}. Must be one of: {sorted(allowed)}")
        return value.upper() if allowed else value

    @classmethod
    def validate_path(cls, path: str, must_exist: bool = False) -> str:
        if not path or not path.strip():
            raise ValueError("Path cannot be empty")
        path = path.strip()
        normalized = os.path.normpath(path)
        if ".." in normalized.split(os.sep):
            raise ValueError("Path traversal not allowed")
        if must_exist and not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        return path

    @classmethod
    def validate_blender_code(cls, code: str) -> str:
        if not code or not code.strip():
            raise ValueError("Code cannot be empty")
        if len(code) > cls.MAX_CODE_LENGTH:
            raise ValueError(f"Code exceeds maximum length of {cls.MAX_CODE_LENGTH} characters")
        return code

    @classmethod
    def check_code_safety(cls, code: str) -> list[str]:
        """Return list of warnings for potentially dangerous code patterns."""
        warnings = []
        for imp in cls.DANGEROUS_IMPORTS:
            if re.search(rf"\bimport\b.*\b{imp}\b|\bfrom\b.*\b{imp}\b", code):
                warnings.append(f"Potentially dangerous import: {imp}")
        for builtin in cls.DANGEROUS_BUILTINS:
            if builtin in code:
                warnings.append(f"Use of restricted builtin: {builtin}")
        if any(kw in code for kw in ["__subclasses__", "__bases__", "__mro__"]):
            warnings.append("Potential sandbox escape attempt detected")
        return warnings

    @classmethod
    def validate_percentage(cls, value: float) -> float:
        return max(0.0, min(100.0, float(value)))

    @classmethod
    def validate_angle(cls, value: float) -> float:
        import math
        return float(value) % (2 * math.pi)
