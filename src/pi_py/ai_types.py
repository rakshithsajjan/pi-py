"""Shared AI-layer types for models, providers, and request context."""

from dataclasses import dataclass
from typing import Literal

from .models import Message

KnownApi = Literal["stub-local", "openai-chat-completions"]
KnownProvider = Literal["stub", "openai"]


@dataclass(frozen=True)
class Model:
    """Model metadata used by provider adapters."""

    id: str
    name: str
    provider: KnownProvider
    api: KnownApi
    base_url: str
    reasoning: bool = False
    max_tokens: int = 4096


@dataclass(frozen=True)
class Context:
    """Provider input context: prompt + ordered conversation messages."""

    messages: list[Message]
    system_prompt: str | None = None

