"""Provider and model adapters.

This module keeps provider-specific details away from the core agent loop.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, Protocol

import httpx

KnownApi = Literal["stub-local", "openai-chat-completions"]
KnownProvider = Literal["stub", "openai"]


class MessageLike(Protocol):
    """Minimal message protocol required by adapters."""

    role: str
    content: str


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
    """Provider input context."""

    messages: list[MessageLike]
    system_prompt: str | None = None


MODELS: dict[KnownProvider, dict[str, Model]] = {
    "stub": {
        "local-minimal": Model(
            id="local-minimal",
            name="Local Minimal Stub",
            provider="stub",
            api="stub-local",
            base_url="local://stub",
            reasoning=False,
            max_tokens=2048,
        )
    },
    "openai": {
        "gpt-4o-mini": Model(
            id="gpt-4o-mini",
            name="GPT-4o mini",
            provider="openai",
            api="openai-chat-completions",
            base_url="https://api.openai.com/v1",
            reasoning=False,
            max_tokens=16384,
        ),
        "gpt-5-mini": Model(
            id="gpt-5-mini",
            name="GPT-5 mini",
            provider="openai",
            api="openai-chat-completions",
            base_url="https://api.openai.com/v1",
            reasoning=True,
            max_tokens=16384,
        ),
    },
}


def get_model(provider: KnownProvider, model_id: str) -> Model:
    """Return one model by provider + model id."""
    model = MODELS.get(provider, {}).get(model_id)
    if model is None:
        raise ValueError(f"unknown model '{provider}/{model_id}'")
    return model


def get_providers() -> list[KnownProvider]:
    """Return available providers."""
    return list(MODELS.keys())


def get_models(provider: KnownProvider) -> list[Model]:
    """Return all models for one provider."""
    return list(MODELS.get(provider, {}).values())


def _get_env_api_key(provider: KnownProvider) -> str | None:
    """Resolve API key from environment for one provider."""
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY")
    return None


def _latest_user_text(messages: list[MessageLike]) -> str:
    """Return latest user message text."""
    for msg in reversed(messages):
        if msg.role == "user":
            return msg.content
    return ""


def _complete_stub_local(model: Model, context: Context, api_key: str | None) -> str:
    """Offline deterministic provider for local development."""
    del model
    del api_key
    user_text = _latest_user_text(context.messages)
    return (
        "You are pi-py, a minimal coding assistant. "
        "Be concise, practical, and explicit about tool usage.\n\n"
        "(stub response)\n"
        f"You said: {user_text}\n"
        "Tool shortcuts: /read <path>, /write <path> <text>, /bash <command>"
    )


def _to_openai_messages(context: Context) -> list[dict[str, str]]:
    """Convert internal messages to OpenAI chat-completions format."""
    out: list[dict[str, str]] = []
    if context.system_prompt:
        out.append({"role": "system", "content": context.system_prompt})
    for msg in context.messages:
        if msg.role in {"user", "assistant"}:
            out.append({"role": msg.role, "content": msg.content})
    return out


def _complete_openai_chat(model: Model, context: Context, api_key: str | None) -> str:
    """Call OpenAI chat-completions and return assistant text."""
    if not api_key:
        raise ValueError("missing OPENAI_API_KEY for provider 'openai'")

    payload = {"model": model.id, "messages": _to_openai_messages(context)}
    with httpx.Client(timeout=60.0) as client:
        response = client.post(
            f"{model.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    choices = data.get("choices", [])
    if not choices:
        return f"(empty model response)\nYou said: {_latest_user_text(context.messages)}"
    return choices[0].get("message", {}).get("content", "") or "(empty text response)"


CompleteFn = Callable[[Model, Context, str | None], str]

API_REGISTRY: dict[KnownApi, CompleteFn] = {
    "stub-local": _complete_stub_local,
    "openai-chat-completions": _complete_openai_chat,
}


def complete_text(
    messages: list[MessageLike],
    provider: KnownProvider,
    model_id: str,
    system_prompt: str,
) -> str:
    """Dispatch one completion request by model.api."""
    model = get_model(provider, model_id)
    context = Context(messages=messages, system_prompt=system_prompt)
    api_key = _get_env_api_key(provider)
    complete_fn = API_REGISTRY.get(model.api)
    if complete_fn is None:
        raise ValueError(f"no adapter registered for api '{model.api}'")
    return complete_fn(model, context, api_key)

