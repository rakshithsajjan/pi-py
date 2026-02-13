"""Shared filesystem helpers for tools."""

from pathlib import Path


def safe_path(cwd: Path, raw: str) -> Path:
    """Resolve user path and reject traversal outside cwd."""
    p = (cwd / raw).resolve()
    cwd_resolved = cwd.resolve()
    if cwd_resolved not in p.parents and p != cwd_resolved:
        raise ValueError(f"path escapes cwd: {raw}")
    return p

