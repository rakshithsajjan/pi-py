"""API registry mapping model APIs to provider adapter functions."""

from collections.abc import Callable

from .ai_types import Context, KnownApi, Model
from .models import Message

CompleteFn = Callable[[Model, Context, str | None], Message]


class ApiProvider:
    """Adapter object with a complete function for one API."""

    def __init__(self, api: KnownApi, complete: CompleteFn) -> None:
        """Store API id and completion function."""
        self.api = api
        self.complete = complete


_api_provider_registry: dict[KnownApi, ApiProvider] = {}


def register_api_provider(provider: ApiProvider) -> None:
    """Register or replace one API provider adapter."""
    _api_provider_registry[provider.api] = provider


def get_api_provider(api: KnownApi) -> ApiProvider | None:
    """Look up a provider adapter by API id."""
    return _api_provider_registry.get(api)


def clear_api_providers() -> None:
    """Remove all registered API providers."""
    _api_provider_registry.clear()

