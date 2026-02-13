# pi-py

Minimal, human-readable Python agent inspired by `pi`.

## Core Philosophy

- Minimal lines of code
- Extremely readable code
- Simple control flow over clever abstractions
- Least dependencies
- Small modules with single responsibility

## Current Scope (v1 scaffold)

- Simple CLI + REPL
- JSONL session persistence
- Tool shortcuts:
  - `/read <path>`
  - `/write <path> <text>`
  - `/bash <command>`
- Local stub LLM response (provider integration comes next)

## v2 Direction

v2 adds richer observability and progress:

- Event stream for every action (`message_start`, `llm_start`, `tool_start`, `tool_stdout_delta`, `tool_end`)
- Better tool/function lifecycle visibility
- Cancellation and run state tracking
- Real LLM provider adapters (OpenAI/Anthropic) with the same simple agent loop

## Project Layout

```text
src/pi_py/
  cli.py        # command-line interface and REPL
  config.py     # config loading + paths
  models.py     # simple data models
  llm.py        # model call boundary (stub now)
  tools.py      # built-in tools
  agent.py      # single-turn agent loop
  session.py    # JSONL session persistence
  prompts.py    # system prompt text
```

## Quick Start (uv)

```bash
uv sync
uv run pi-py "hello"
uv run pi-py
```

Try a tool command:

```bash
uv run pi-py "/bash ls -la"
```

In v1, command output is returned as a normal assistant response. Structured event/progress streams are part of v2.

## Why `uv`?

`uv` is a fast Python project/dependency manager. For this project it keeps setup simple:

- fast env + installs
- reproducible dependencies
- one command runner (`uv run ...`)
