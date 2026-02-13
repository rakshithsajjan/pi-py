from pathlib import Path

from .events import Event, EventBus
from .llm import complete
from .models import AgentState, Message
from .tools import run_tool_shortcut


class Agent:
    def __init__(self, cwd: Path, events: EventBus | None = None) -> None:
        self.cwd = cwd
        self.events = events or EventBus()
        self.state = AgentState()

    def run_turn(self, user_text: str) -> Message:
        user = Message(role="user", content=user_text)
        self.state.messages.append(user)
        self.events.emit(Event(type="message_start", payload={"role": "user", "text": user_text}))

        tool_result = run_tool_shortcut(self.cwd, user_text, self.events)
        if tool_result is not None:
            assistant = Message(role="assistant", content=tool_result)
            self.state.messages.append(assistant)
            self.events.emit(Event(type="message_end", payload={"role": "assistant", "tool_shortcut": True}))
            return assistant

        self.events.emit(Event(type="llm_start"))
        assistant = complete(self.state.messages)
        self.state.messages.append(assistant)
        self.events.emit(Event(type="llm_end"))
        self.events.emit(Event(type="message_end", payload={"role": "assistant", "tool_shortcut": False}))
        return assistant

