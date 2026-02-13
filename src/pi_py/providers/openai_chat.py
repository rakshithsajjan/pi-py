"""OpenAI chat-completions provider adapter."""

import httpx

from . import shared
from ..ai_types import Context, Model
from ..models import Message


def _to_openai_messages(context: Context) -> list[dict[str, str]]:
    """Convert internal messages into OpenAI Chat Completions message format."""
    out: list[dict[str, str]] = []
    if context.system_prompt:
        out.append({"role": "system", "content": context.system_prompt})
    for msg in context.messages:
        if msg.role in {"user", "assistant"}:
            out.append({"role": msg.role, "content": msg.content})
    return out


def complete_openai_chat(model: Model, context: Context, api_key: str | None) -> Message:
    """Call OpenAI Chat Completions and return one assistant message."""
    if not api_key:
        raise ValueError("missing OPENAI_API_KEY for provider 'openai'")

    payload = {
        "model": model.id,
        "messages": _to_openai_messages(context),
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{model.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    choices = data.get("choices", [])
    if not choices:
        fallback = shared.latest_user_text(context.messages)
        return Message(role="assistant", content=f"(empty model response)\nYou said: {fallback}")

    content = choices[0].get("message", {}).get("content", "")
    return Message(role="assistant", content=content or "(empty text response)")

