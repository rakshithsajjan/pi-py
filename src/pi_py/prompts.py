def system_prompt() -> str:
    """Base behavior instructions sent to the model layer."""
    return (
        "You are pi-py, a minimal coding assistant. "
        "Be concise, practical, and explicit about tool usage."
    )
