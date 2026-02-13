import argparse
from pathlib import Path

from .agent import Agent
from .config import load_config
from .session import append_message, load_messages, new_session_path


def main() -> None:
    """CLI entrypoint: run one prompt or start a simple REPL loop."""
    parser = argparse.ArgumentParser(description="pi-py: minimal Python coding agent")
    parser.add_argument("prompt", nargs="?", help="single prompt (if omitted, enters repl)")
    parser.add_argument("--session", help="path to existing session jsonl")
    args = parser.parse_args()

    cfg = load_config()
    session_path = Path(args.session) if args.session else new_session_path(cfg.sessions_dir)

    agent = Agent(cwd=cfg.cwd)

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
