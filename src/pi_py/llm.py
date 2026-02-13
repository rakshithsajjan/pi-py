"""LLM boundary for agent code.

Keeps the rest of the codebase provider-agnostic.
"""

from .ai_types import Context, KnownProvider
from .env_api_keys import get_env_api_key
from .model_registry import get_model
from .models import Message
from .prompts import system_prompt
from .stream import complete as dispatch_complete


def complete(messages: list[Message], provider: KnownProvider, model_id: str) -> Message:
    """Resolve a model + provider adapter and return one assistant response."""
    model = get_model(provider, model_id)
    context = Context(messages=messages, system_prompt=system_prompt())
    api_key = get_env_api_key(provider)
    return dispatch_complete(model, context, api_key)
