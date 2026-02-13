from pathlib import Path

from .ai_types import KnownProvider
from .llm import complete
from .model_registry import get_model
from .models import AgentState, Message
from .tools import run_tool_shortcut


class Agent:
    """Small orchestration layer for one-turn agent execution."""

    def __init__(self, cwd: Path, provider: KnownProvider = "stub", model_id: str = "local-minimal") -> None:
        """Initialize an agent bound to one workspace directory."""
        self.cwd = cwd
        # Validate model selection at startup for fast feedback.
        get_model(provider, model_id)
        self.provider = provider
        self.model_id = model_id
        self.state = AgentState()

    def run_turn(self, user_text: str) -> Message:
        """Process one user message and return one assistant message."""
        user = Message(role="user", content=user_text)
        self.state.messages.append(user)

        tool_result = run_tool_shortcut(self.cwd, user_text)
        if tool_result is not None:
            assistant = Message(role="assistant", content=tool_result)
            self.state.messages.append(assistant)
            return assistant

        assistant = complete(self.state.messages, provider=self.provider, model_id=self.model_id)
        self.state.messages.append(assistant)
        return assistant
