from .models import Message
from .prompts import system_prompt


def complete(messages: list[Message]) -> Message:
    """Return an assistant message from the current conversation.

    This is intentionally a local stub for now. In the next iteration,
    this function becomes the provider boundary (OpenAI/Anthropic calls).
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
