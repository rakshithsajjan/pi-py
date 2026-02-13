# pi-py agent.md

This document defines how `pi-py` should evolve.

Inspired by:
- Armin Ronacher, “Pi: The Minimal Agent Within OpenClaw” (January 31, 2026)
- https://lucumr.pocoo.org/2026/1/31/pi/

## Core Philosophy

`pi-py` should stay:
- Minimal
- Readable
- Reliable
- Hackable by the agent itself

We prefer a tiny core over a huge built-in feature set.

## Product Principles

1. Keep the core small.
- The core loop should remain easy to read in one sitting.
- New behavior should default to extensions, not core bloat.

2. Treat code execution as the main superpower.
- The agent should be good at writing code and running code.
- If a feature is missing, prefer implementing it in-repo over adding complex external machinery.

3. Build for self-extension.
- The agent should be able to improve itself by editing local code.
- Extension and skill workflows should be first-class.

4. Keep sessions portable.
- Session data should be provider-agnostic as much as possible.
- Avoid deep coupling to one model vendor’s proprietary format.

5. Prefer tools outside context when possible.
- Use CLI/skills/extensions for many capabilities.
- Add model-visible tools only when needed for the task.

6. Prioritize reliability over novelty.
- Stable behavior, predictable output, and low memory use matter more than flashy features.

## Architecture Rules

1. Keep a layered structure.
- `model catalog` -> `model lookup` -> `api registry` -> `provider adapter` -> `dispatch`.

2. Keep providers isolated.
- Provider-specific logic belongs in `src/pi_py/providers/*`.
- Shared model/runtime code must not depend on one provider’s quirks.

3. Use deterministic generation.
- Generated files (such as model catalogs) must be reproducible and sorted.

4. Design for branchable sessions.
- Session format should support future branching, rewind, and summaries.
- Do not lock us into flat linear logs forever.

## Simplicity Constraints

1. Minimize dependencies.
- Add a dependency only if it clearly removes complexity.
- Prefer stdlib-first implementations.

2. Keep modules small.
- Functions should be straightforward and explicit.
- Avoid deep inheritance or framework-heavy abstractions.

3. Favor explicit data models.
- Keep message/session/provider types simple and documented.

## Extension Direction

`pi-py` should support:
- Slash-like workflows
- Local skills
- Lightweight extension hooks
- Extension state persistence in session data

But this should be incremental. Start with a tiny hook surface and grow from real usage.

## Non-Goals (for now)

- A giant built-in tool ecosystem
- Heavy orchestration frameworks
- Large UI-first complexity before core reliability

## Development Workflow

1. Build in small increments.
2. Keep tests focused and readable.
3. Document behavior in plain language.
4. Use `uv` for environment, dependency, and run workflows.

## Decision Heuristic

When choosing between two designs, prefer the one that:
- Is easier for a beginner to understand
- Keeps the core smaller
- Keeps behavior more deterministic
- Lets the agent extend itself through code

