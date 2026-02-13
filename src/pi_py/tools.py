import shlex
import subprocess
from pathlib import Path


def _safe_path(cwd: Path, raw: str) -> Path:
    """Resolve a user path and block access outside the workspace."""
    p = (cwd / raw).resolve()
    cwd_resolved = cwd.resolve()
    if cwd_resolved not in p.parents and p != cwd_resolved:
        raise ValueError(f"path escapes cwd: {raw}")
    return p


def tool_read(cwd: Path, path: str) -> str:
    """Read UTF-8 file content inside the workspace."""
    p = _safe_path(cwd, path)
    return p.read_text(encoding="utf-8")


def tool_write(cwd: Path, path: str, text: str) -> str:
    """Write UTF-8 text to a file inside the workspace."""
    p = _safe_path(cwd, path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return f"wrote {len(text)} chars to {p}"


def tool_bash(cwd: Path, command: str) -> str:
    """Run a shell command and return stdout (or error output)."""
    proc = subprocess.Popen(
        command,
        cwd=str(cwd),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout_parts: list[str] = []
    stderr_parts: list[str] = []

    assert proc.stdout is not None
    assert proc.stderr is not None

    for line in proc.stdout:
        stdout_parts.append(line)

    for line in proc.stderr:
        stderr_parts.append(line)

    code = proc.wait()
    result = "".join(stdout_parts).strip()
    error = "".join(stderr_parts).strip()
    if code != 0:
        return f"bash failed ({code})\n{error}"
    return result or "(no output)"


def run_tool_shortcut(cwd: Path, text: str) -> str | None:
    """Parse slash shortcuts and route to a built-in tool handler."""
    if text.startswith("/read "):
        path = text[len("/read ") :].strip()
        return tool_read(cwd, path)

    if text.startswith("/write "):
        parts = shlex.split(text)
        if len(parts) < 3:
            return "usage: /write <path> <text>"
        _, path, *rest = parts
        return tool_write(cwd, path, " ".join(rest))

    if text.startswith("/bash "):
        command = text[len("/bash ") :].strip()
        return tool_bash(cwd, command)

    return None
