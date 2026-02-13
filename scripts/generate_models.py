"""Generate src/pi_py/models_generated.py.

This starter version keeps generation simple and deterministic.
For now it rewrites a static template so the workflow exists early.
"""

from pathlib import Path


def generate() -> None:
    """Write a deterministic model catalog file used by model_registry.py."""
    project_root = Path(__file__).resolve().parent.parent
    target = project_root / "src" / "pi_py" / "models_generated.py"
    content = """\"\"\"Auto-generated model catalog placeholder.

In future versions this can be written by scripts/generate_models.py.
\"\"\"

from .ai_types import Model

MODELS: dict[str, dict[str, Model]] = {
    \"stub\": {
        \"local-minimal\": Model(
            id=\"local-minimal\",
            name=\"Local Minimal Stub\",
            provider=\"stub\",
            api=\"stub-local\",
            base_url=\"local://stub\",
            reasoning=False,
            max_tokens=2048,
        )
    },
    \"openai\": {
        \"gpt-4o-mini\": Model(
            id=\"gpt-4o-mini\",
            name=\"GPT-4o mini\",
            provider=\"openai\",
            api=\"openai-chat-completions\",
            base_url=\"https://api.openai.com/v1\",
            reasoning=False,
            max_tokens=16384,
        ),
        \"gpt-5-mini\": Model(
            id=\"gpt-5-mini\",
            name=\"GPT-5 mini\",
            provider=\"openai\",
            api=\"openai-chat-completions\",
            base_url=\"https://api.openai.com/v1\",
            reasoning=True,
            max_tokens=16384,
        ),
    },
}
"""
    target.write_text(content, encoding="utf-8")
    print(f"Generated {target}")


if __name__ == "__main__":
    generate()

