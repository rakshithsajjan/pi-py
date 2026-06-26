# pi-py: Python Equivalent of pi.dev Coding Agent

Build a Python equivalent of [pi.dev](https://pi.dev/)'s coding agent from the fundamentals up.

## Why From Scratch?

Not vibe coding. Not porting line-by-line. We're building the same primitives pi uses — function calling, tool use, context engineering, caching, session trees — but in Python, understanding every layer as we go.

## Philosophy

Adapted from [pi.dev's philosophy](https://pi.dev/) and [agent.md](https://lucumr.pocoo.org/2026/1/31/pi/):

### Keep the core small
- The agent loop should be readable in one sitting
- New behavior defaults to extensions, not core bloat

### Code execution as superpower
- Write code and run code
- Missing a feature? Implement it in-repo over adding complex machinery

### Build for self-extension
- The agent improves itself by editing its own source
- Extension and skill workflows are first-class

### Minimize dependencies
- `httpx` is the only non-stdlib dependency (for now)
- Prefer stdlib-first implementations

## Architecture

```
user message
  → context builder (system prompt + AGENTS.md + messages + tools)
  → LLM provider (streaming, tool calls)
  → parse tool calls
  → execute tools (read/write/bash/edit/grep/find/ls)
  → loop or respond
  → persist to session
```

### Layers

| Layer | Responsibility |
|---|---|
| `cli/` | Entrypoint, args, REPL, print/JSON/RPC modes |
| `core/` | Agent loop, Message/ToolCall models, session management |
| `tools/` | Tool definitions with JSON Schema, registry, executors |
| `providers/` | LLM adapters — stub, OpenAI, Anthropic, Google, Ollama |
| `context/` | System prompt builder, AGENTS.md, skills, compaction |
| `cache/` | Prompt caching layer (Anthropic style, OpenAI style) |

### Tool Architecture

Each tool = `name` + `description` + `parameters` (JSON Schema) + `executor(cwd, args) → str`

Tools are registered in a `ToolRegistry`. The agent loop:
1. Exposes tools via the LLM's function calling API
2. LLM responds with `tool_call` blocks
3. Loop executes each tool, collects results
4. Sends results back to LLM
5. LLM continues or responds

Built-in tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`

### Provider Architecture

Each provider implements `stream(messages, tools, config)` yielding events:

```
TextDelta(content) | ToolCallStart(id, name, args) | ToolCallEnd(id, result) | Error(message)
```

Streaming-first. Non-streaming is a convenience wrapper over streaming.

### Caching

- Anthropic: prompt caching via `cache_control` breakpoints on system + messages
- OpenAI: context caching via `cached_content` markers
- Automatic: detect, mark, clear caches based on token thresholds

### Session System

- JSONL with tree support: each entry has `id` and `parent_id`
- Branching without creating new files — `/tree` navigation
- Compaction: summarize older messages on context overflow
- Bookmarking, filtering, export

### Context Engineering

- `AGENTS.md` / `CLAUDE.md` loaded from cwd and parent dirs
- `SYSTEM.md` to replace default system prompt
- `APPEND_SYSTEM.md` to append
- Skills: on-demand capability packages loaded via `/skill:name`
- Prompt templates: Markdown expanded via `/template-name`

## Implementation Phases

### Phase 1 — Core Loop (current)
- Agent loop: think → tool calls → execute → loop or respond
- Tool system: definitions, registry, executors
- Stub provider for offline testing
- CLI: `pi-py -p "query"` (print mode) and `pi-py` (REPL)

### Phase 2 — Real Providers
- OpenAI provider with streaming
- Anthropic provider with streaming
- Prompt caching integration

### Phase 3 — Sessions & Context
- JSONL session persistence (tree format)
- Context builder with system prompt + AGENTS.md
- Auto-compaction

### Phase 4 — Full Feature Set
- More providers: Google Gemini, Ollama, Groq
- Skills and prompt templates
- Extension system
- JSON and RPC modes

## Reference

The TypeScript reference source lives at `ref/pi/`. See [ref/pi/SOURCE.md](ref/pi/SOURCE.md) for details.

## Development

```bash
uv run pi-py -p "hello"          # print mode
uv run pi-py                     # REPL
uv run pi-py --list-models       # list available models
uv run pytest                    # run tests
```

## License

MIT
