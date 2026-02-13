"""Core agent runtime with minimal dependencies and explicit control flow."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .adapters import KnownProvider, complete_text, get_model
from .tools import run_tool_shortcut


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
