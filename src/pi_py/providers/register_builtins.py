"""Register built-in API providers."""

from ..api_registry import ApiProvider, clear_api_providers, register_api_provider
from .openai_chat import complete_openai_chat
from .stub_local import complete_stub_local


def register_built_in_api_providers() -> None:
    """Register all built-in API adapters."""
    register_api_provider(ApiProvider(api="stub-local", complete=complete_stub_local))
    register_api_provider(ApiProvider(api="openai-chat-completions", complete=complete_openai_chat))


def reset_api_providers() -> None:
    """Clear registry then register all built-in adapters again."""
    clear_api_providers()
    register_built_in_api_providers()


register_built_in_api_providers()

