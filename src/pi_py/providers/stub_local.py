"""Local stub provider for offline development and demos."""

from . import shared
from ..ai_types import Context, Model
from ..models import Message


def complete_stub_local(model: Model, context: Context, api_key: str | None) -> Message:
    """Return a deterministic local assistant response without network calls."""
    del model
    del api_key
    user_text = shared.latest_user_text(context.messages)
    text = (
        "You are pi-py, a minimal coding assistant. "
        "Be concise, practical, and explicit about tool usage.\n\n"
        "(stub response)\n"
        f"You said: {user_text}\n"
        "Tool shortcuts: /read <path>, /write <path> <text>, /bash <command>"
    )
    return Message(role="assistant", content=text)

