import argparse
from pathlib import Path
from typing import cast

from .adapters import KnownProvider, get_models, get_providers
from .core import Agent, append_message, load_config, load_messages, new_session_path


def main() -> None:
    """CLI entrypoint: run one prompt or start a simple REPL loop."""
    parser = argparse.ArgumentParser(description="pi-py: minimal Python coding agent")
    parser.add_argument("prompt", nargs="?", help="single prompt (if omitted, enters repl)")
    parser.add_argument("--session", help="path to existing session jsonl")
    parser.add_argument("--provider", default="stub", help="model provider (e.g. stub, openai)")
    parser.add_argument("--model", default="local-minimal", help="model id for chosen provider")
    parser.add_argument("--list-models", action="store_true", help="list available providers/models and exit")
    args = parser.parse_args()

    if args.list_models:
        for provider in get_providers():
            print(f"{provider}:")
            for model in get_models(provider):
                print(f"  - {model.id}")
        return

    cfg = load_config()
    session_path = Path(args.session) if args.session else new_session_path(cfg.sessions_dir)

    provider = args.provider
    if provider not in get_providers():
        choices = ", ".join(get_providers())
        raise ValueError(f"unknown provider '{provider}'. choose one of: {choices}")

    agent = Agent(cwd=cfg.cwd, provider=cast(KnownProvider, provider), model_id=args.model)

    for m in load_messages(session_path):
        agent.state.messages.append(m)

    if args.prompt:
        try:
            reply = agent.run_turn(args.prompt)
        except Exception as exc:
            print(f"error: {exc}")
            return
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
        try:
            reply = agent.run_turn(text)
        except Exception as exc:
            print(f"error: {exc}")
            continue
        append_message(session_path, agent.state.messages[-2])  # user
        append_message(session_path, reply)
        print(reply.content)
