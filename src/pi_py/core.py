"""Core agent runtime with minimal dependencies and explicit control flow."""

from __future__ import annotations

import json
import shlex
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .adapters import KnownProvider, complete_text, get_model


def now_iso() -> str:
    """Return current UTC timestamp as ISO-8601 text."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Message:
    """Single chat message stored in memory and session files."""

    role: str
    content: str
    timestamp: str = field(default_factory=now_iso)


@dataclass
class AgentState:
    """Minimal mutable state for one session."""

    messages: list[Message] = field(default_factory=list)


@dataclass
class Config:
    """Runtime paths and filesystem settings for a run."""

    cwd: Path
    sessions_dir: Path


def load_config(cwd: Path | None = None) -> Config:
    """Create config and ensure session directory exists."""
    base = cwd or Path.cwd()
    sessions_dir = base / ".pi_py" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return Config(cwd=base, sessions_dir=sessions_dir)


def system_prompt() -> str:
    """Base model behavior instructions."""
    return (
        "You are pi-py, a minimal coding assistant. "
        "Be concise, practical, and explicit about tool usage."
    )


def new_session_path(sessions_dir: Path) -> Path:
    """Return timestamped JSONL path for a new session."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return sessions_dir / f"{stamp}.jsonl"


def append_message(path: Path, message: Message) -> None:
    """Append one message to JSONL session storage."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"role": message.role, "content": message.content, "timestamp": message.timestamp}))
        f.write("\n")


def load_messages(path: Path) -> list[Message]:
    """Load JSONL session messages."""
    if not path.exists():
        return []
    out: list[Message] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            out.append(
                Message(
                    role=row.get("role", "user"),
                    content=row.get("content", ""),
                    timestamp=row.get("timestamp", now_iso()),
                )
            )
    return out


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


def run_tool_shortcut(cwd: Path, text: str) -> str | None:
    """Handle /read /write /bash shortcuts, or return None."""
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


class Agent:
    """Single-turn orchestrator: user message -> tool or provider response."""

    def __init__(self, cwd: Path, provider: KnownProvider = "stub", model_id: str = "local-minimal") -> None:
        """Initialize agent with working directory and model selection."""
        get_model(provider, model_id)
        self.cwd = cwd
        self.provider = provider
        self.model_id = model_id
        self.state = AgentState()

    def run_turn(self, user_text: str) -> Message:
        """Process one user turn and return one assistant message."""
        user = Message(role="user", content=user_text)
        self.state.messages.append(user)

        tool_result = run_tool_shortcut(self.cwd, user_text)
        if tool_result is not None:
            assistant = Message(role="assistant", content=tool_result)
            self.state.messages.append(assistant)
            return assistant

        assistant_text = complete_text(
            messages=self.state.messages,
            provider=self.provider,
            model_id=self.model_id,
            system_prompt=system_prompt(),
        )
        assistant = Message(role="assistant", content=assistant_text)
        self.state.messages.append(assistant)
        return assistant
