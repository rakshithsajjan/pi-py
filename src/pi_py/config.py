from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    cwd: Path
    sessions_dir: Path


def load_config(cwd: Path | None = None) -> Config:
    base = cwd or Path.cwd()
    sessions_dir = base / ".pi_py" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return Config(cwd=base, sessions_dir=sessions_dir)

