"""Write tool."""

from pathlib import Path

from .path_utils import safe_path


def tool_write(cwd: Path, path: str, text: str) -> str:
    """Write UTF-8 text file."""
    p = safe_path(cwd, path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return f"wrote {len(text)} chars to {p}"

