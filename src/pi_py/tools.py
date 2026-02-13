import shlex
import subprocess
from pathlib import Path

from .events import Event, EventBus


def _safe_path(cwd: Path, raw: str) -> Path:
    p = (cwd / raw).resolve()
    cwd_resolved = cwd.resolve()
    if cwd_resolved not in p.parents and p != cwd_resolved:
        raise ValueError(f"path escapes cwd: {raw}")
    return p


def tool_read(cwd: Path, path: str) -> str:
    p = _safe_path(cwd, path)
    return p.read_text(encoding="utf-8")


def tool_write(cwd: Path, path: str, text: str) -> str:
    p = _safe_path(cwd, path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return f"wrote {len(text)} chars to {p}"


def tool_bash(cwd: Path, command: str, events: EventBus) -> str:
    events.emit(Event(type="tool_start", payload={"tool": "bash", "command": command}))
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
        events.emit(Event(type="tool_stdout_delta", payload={"line": line.rstrip("\n")}))

    for line in proc.stderr:
        stderr_parts.append(line)
        events.emit(Event(type="tool_stderr_delta", payload={"line": line.rstrip("\n")}))

    code = proc.wait()
    result = "".join(stdout_parts).strip()
    error = "".join(stderr_parts).strip()
    events.emit(Event(type="tool_end", payload={"tool": "bash", "exit_code": code}))
    if code != 0:
        return f"bash failed ({code})\n{error}"
    return result or "(no output)"


def run_tool_shortcut(cwd: Path, text: str, events: EventBus) -> str | None:
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
        return tool_bash(cwd, command, events)

    return None

