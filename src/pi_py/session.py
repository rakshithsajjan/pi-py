import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Message


def new_session_path(sessions_dir: Path) -> Path:
    """Return a timestamped JSONL path for a new session."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return sessions_dir / f"{stamp}.jsonl"


def append_message(path: Path, message: Message) -> None:
    """Append one message entry to a JSONL session file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"role": message.role, "content": message.content, "timestamp": message.timestamp}))
        f.write("\n")


def load_messages(path: Path) -> list[Message]:
    """Load all messages from a JSONL session file."""
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
                    timestamp=row.get("timestamp", datetime.now(timezone.utc).isoformat()),
                )
            )
    return out
