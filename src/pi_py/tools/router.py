"""Shortcut router for built-in tools."""

import shlex
from pathlib import Path

from .bash import tool_bash
from .read import tool_read
from .time import tool_time_utc
from .write import tool_write


def run_tool_shortcut(cwd: Path, text: str) -> str | None:
    """Handle /read /write /bash /time shortcuts, or return None."""
    if text.strip() == "/time":
        return tool_time_utc()
    if text.startswith("/read "):
        return tool_read(cwd, text[len("/read ") :].strip())
    if text.startswith("/write "):
        parts = shlex.split(text)
        if len(parts) < 3:
            return "usage: /write <path> <text>"
        _, path, *rest = parts
        return tool_write(cwd, path, " ".join(rest))
    if text.startswith("/bash "):
        return tool_bash(cwd, text[len("/bash ") :].strip())
    return None

