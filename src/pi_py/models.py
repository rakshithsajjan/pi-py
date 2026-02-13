from dataclasses import dataclass, field
from datetime import datetime, timezone


def now_iso() -> str:
    """Return the current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Message:
    """Single chat message stored in memory and session files."""

    role: str
    content: str
    timestamp: str = field(default_factory=now_iso)


@dataclass
class AgentState:
    """Minimal mutable state used by the agent loop."""

    messages: list[Message] = field(default_factory=list)
