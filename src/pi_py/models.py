from dataclasses import dataclass, field
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Message:
    role: str
    content: str
    timestamp: str = field(default_factory=now_iso)


@dataclass
class AgentState:
    messages: list[Message] = field(default_factory=list)

