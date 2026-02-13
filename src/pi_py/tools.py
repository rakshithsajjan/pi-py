"""All built-in tools in one module."""

import shlex
import subprocess
from pathlib import Path
from datetime import datetime, timezone


def _safe_path(cwd: Path, raw: str) -> Path:
    """Resolve user path and reject traversal outside cwd."""
    p = (cwd / raw).resolve()
    cwd_resolved = cwd.resolve()
    if cwd_resolved not in p.parents and p != cwd_resolved:
        raise ValueError(f"path escapes cwd: {raw}")
    return p


def tool_read(cwd: Path, path: str) -> str:
    """Read UTF-8 text file."""
    return _safe_path(cwd, path).read_text(encoding="utf-8")


def tool_write(cwd: Path, path: str, text: str) -> str:
    """Write UTF-8 text file."""
    p = _safe_path(cwd, path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return f"wrote {len(text)} chars to {p}"


def tool_bash(cwd: Path, command: str) -> str:
    """Run one shell command and return output text."""
    proc = subprocess.Popen(
        command,
        cwd=str(cwd),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout is not None
    assert proc.stderr is not None
    out = "".join(proc.stdout.readlines()).strip()
    err = "".join(proc.stderr.readlines()).strip()
    code = proc.wait()
    if code != 0:
        return f"bash failed ({code})\n{err}"
    return out or "(no output)"


def tool_time_utc() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


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

