from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Runtime paths and filesystem settings for a pi-py run."""

    cwd: Path
    sessions_dir: Path


def load_config(cwd: Path | None = None) -> Config:
    """Create config and ensure the session directory exists."""
    base = cwd or Path.cwd()
    sessions_dir = base / ".pi_py" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return Config(cwd=base, sessions_dir=sessions_dir)
