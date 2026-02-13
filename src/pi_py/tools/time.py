"""Time tool."""

from datetime import datetime, timezone


def tool_time_utc() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()

