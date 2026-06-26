# pi-py

From-scratch Python equivalent of [pi.dev](https://pi.dev/)'s coding agent.

Built on fundamentals: function calling, tool use, context engineering, session management, caching, streaming.

```bash
uv run pi-py
```

This is a **greenfield rebuild** (v2.0). The old v0.1 code is preserved on the `old-v0.1` branch. Everything here is built from the ground up. See [GOAL.md](GOAL.md) for the full vision.

## Quick Start

```bash
uv sync
uv run pi-py -p "hello"          # stub provider
uv run pi-py                     # REPL mode
uv run pi-py --list-models       # see available models
```

## Reference

The TypeScript pi source is in `ref/pi/` for architecture study. See [ref/pi/SOURCE.md](ref/pi/SOURCE.md).
