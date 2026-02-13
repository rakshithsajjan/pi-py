from pathlib import Path

from pi_py.core import Agent


def test_agent_stub_turn() -> None:
    agent = Agent(cwd=Path("."), provider="stub", model_id="local-minimal")
    reply = agent.run_turn("hello")
    assert reply.role == "assistant"
    assert "(stub response)" in reply.content


def test_agent_tool_shortcut_turn(tmp_path) -> None:
    agent = Agent(cwd=tmp_path, provider="stub", model_id="local-minimal")
    reply = agent.run_turn("/bash echo from-tool")
    assert "from-tool" in reply.content
