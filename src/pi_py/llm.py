from .models import Message
from .prompts import system_prompt


def complete(messages: list[Message]) -> Message:
    """
    Minimal local stub.
    Replace this with a provider call in v1.1 (OpenAI/Anthropic).
    """
    user_text = ""
    for msg in reversed(messages):
        if msg.role == "user":
            user_text = msg.content
            break

    text = (
        f"{system_prompt()}\n\n"
        f"(stub response)\n"
        f"You said: {user_text}\n"
        "Tool shortcuts: /read <path>, /write <path> <text>, /bash <command>"
    )
    return Message(role="assistant", content=text)

