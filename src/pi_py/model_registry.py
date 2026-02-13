"""Model lookup functions backed by the generated model catalog."""

from .ai_types import KnownProvider, Model
from .models_generated import MODELS


def get_model(provider: KnownProvider, model_id: str) -> Model:
    """Return one model by provider + model id, or raise a clear error."""
    provider_models = MODELS.get(provider, {})
    model = provider_models.get(model_id)
    if model is None:
        raise ValueError(f"unknown model '{provider}/{model_id}'")
    return model


def get_providers() -> list[KnownProvider]:
    """Return available provider names."""
    return list(MODELS.keys())  # type: ignore[return-value]


def get_models(provider: KnownProvider) -> list[Model]:
    """Return all models for one provider."""
    return list(MODELS.get(provider, {}).values())

