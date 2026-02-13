"""Top-level dispatch from model.api to the registered provider adapter."""

# Ensure built-in providers are registered on import.
from .providers import register_builtins as _register_builtins  # noqa: F401

from .ai_types import Context, Model
from .api_registry import get_api_provider
from .models import Message


def complete(model: Model, context: Context, api_key: str | None) -> Message:
    """Dispatch completion call to the provider registered for model.api."""
    provider = get_api_provider(model.api)
    if provider is None:
        raise ValueError(f"no API provider registered for api '{model.api}'")
    return provider.complete(model, context, api_key)

