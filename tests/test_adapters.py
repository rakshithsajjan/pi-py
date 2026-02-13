from pi_py.adapters import complete_text, get_model, get_models, get_providers
from pi_py.core import Message


def test_get_providers_contains_stub_and_openai() -> None:
    providers = get_providers()
    assert "stub" in providers
    assert "openai" in providers


def test_get_models_for_stub() -> None:
    models = get_models("stub")
    assert any(m.id == "local-minimal" for m in models)


def test_get_model_unknown_raises() -> None:
    try:
        get_model("stub", "does-not-exist")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "unknown model" in str(exc)


def test_complete_text_stub_path() -> None:
    messages = [Message(role="user", content="hello")]
    text = complete_text(messages=messages, provider="stub", model_id="local-minimal", system_prompt="test")
    assert "(stub response)" in text
    assert "hello" in text

