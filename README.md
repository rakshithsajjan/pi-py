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
- TS-style model/provider architecture:
  - model catalog (`models_generated.py`)
  - model lookup (`model_registry.py`)
  - API registry (`api_registry.py`)
  - provider adapters (`providers/*`)
  - dispatch boundary (`stream.py`)
- Tool shortcuts:
  - `/read <path>`
  - `/write <path> <text>`
  - `/bash <command>`
- Providers:
  - `stub/local-minimal` (offline default)
  - `openai/gpt-4o-mini`, `openai/gpt-5-mini`

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
  ai_types.py   # model/provider/context types
  models_generated.py  # generated model catalog
  model_registry.py    # get_model/get_models/get_providers
  env_api_keys.py      # provider -> env var key lookup
  api_registry.py      # api -> adapter registry
  config.py     # config loading + paths
  models.py     # simple data models
  llm.py        # model/provider dispatch boundary for agent
  stream.py     # generic dispatch by model.api
  providers/    # provider adapters and built-in registration
  tools.py      # built-in tools
  agent.py      # single-turn agent loop
  session.py    # JSONL session persistence
  prompts.py    # system prompt text
scripts/
  generate_models.py   # deterministic model-catalog generator
```

## Quick Start (uv)

```bash
uv sync
uv run pi-py "hello"
uv run pi-py
uv run pi-py --list-models
```

Try a tool command:

```bash
uv run pi-py "/bash ls -la"
```

Use OpenAI provider:

```bash
export OPENAI_API_KEY=your_key_here
uv run pi-py --provider openai --model gpt-4o-mini "Write a haiku about clean code"
```

In v1, command output is returned as a normal assistant response. Structured event/progress streams remain part of v2.

## Why `uv`?

`uv` is a fast Python project/dependency manager. For this project it keeps setup simple:

- fast env + installs
- reproducible dependencies
- one command runner (`uv run ...`)
