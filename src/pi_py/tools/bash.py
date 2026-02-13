"""Bash tool."""

import subprocess
from pathlib import Path


def tool_bash(cwd: Path, command: str) -> str:
    """Run one shell command and return output text."""
    proc = subprocess.Popen(
        command,
        cwd=str(cwd),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdout is not None
    assert proc.stderr is not None
    out = "".join(proc.stdout.readlines()).strip()
    err = "".join(proc.stderr.readlines()).strip()
    code = proc.wait()
    if code != 0:
        return f"bash failed ({code})\n{err}"
    return out or "(no output)"

