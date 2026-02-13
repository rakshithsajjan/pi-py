"""Centralized environment-variable lookup for provider credentials."""

import os

from .ai_types import KnownProvider


def get_env_api_key(provider: KnownProvider) -> str | None:
    """Return API key from environment variables for a provider."""
    env_map: dict[KnownProvider, str] = {
        "stub": "",
        "openai": "OPENAI_API_KEY",
    }
    env_var = env_map[provider]
    if not env_var:
        return None
    return os.getenv(env_var)

