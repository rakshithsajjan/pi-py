"""Shared helper functions used by provider adapters."""

from ..models import Message


def latest_user_text(messages: list[Message]) -> str:
    """Return the latest user message text, or empty string."""
    for msg in reversed(messages):
        if msg.role == "user":
            return msg.content
    return ""

