import argparse
import json
from pathlib import Path

from .agent import Agent
from .config import load_config
from .events import Event
from .session import append_message, load_messages, new_session_path


def _print_event(event: Event) -> None:
    if event.type in {"tool_start", "tool_end"}:
        print(f"[event] {event.type}: {json.dumps(event.payload)}")
    if event.type == "tool_stdout_delta":
        line = event.payload.get("line", "")
        if line:
            print(f"[stdout] {line}")
    if event.type == "tool_stderr_delta":
        line = event.payload.get("line", "")
        if line:
            print(f"[stderr] {line}")


def main() -> None:
    parser = argparse.ArgumentParser(description="pi-py: minimal Python coding agent")
    parser.add_argument("prompt", nargs="?", help="single prompt (if omitted, enters repl)")
    parser.add_argument("--session", help="path to existing session jsonl")
    parser.add_argument("--no-events", action="store_true", help="disable event printing")
    args = parser.parse_args()

    cfg = load_config()
    session_path = Path(args.session) if args.session else new_session_path(cfg.sessions_dir)

    agent = Agent(cwd=cfg.cwd)
    if not args.no_events:
        agent.events.subscribe(_print_event)

    for m in load_messages(session_path):
        agent.state.messages.append(m)

    if args.prompt:
        reply = agent.run_turn(args.prompt)
        append_message(session_path, agent.state.messages[-2])  # user
        append_message(session_path, reply)
        print(reply.content)
        return

    print("pi-py repl. type 'exit' to quit.")
    while True:
        try:
            text = input("> ").strip()
        except EOFError:
            print()
            break
        if text in {"exit", "quit"}:
            break
        if not text:
            continue
        reply = agent.run_turn(text)
        append_message(session_path, agent.state.messages[-2])  # user
        append_message(session_path, reply)
        print(reply.content)

