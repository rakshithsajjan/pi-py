"""Read tool."""

from pathlib import Path

from .path_utils import safe_path


def tool_read(cwd: Path, path: str) -> str:
    """Read UTF-8 text file."""
    return safe_path(cwd, path).read_text(encoding="utf-8")

