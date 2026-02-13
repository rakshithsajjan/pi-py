from pathlib import Path

from pi_py.tools.bash import tool_bash
from pi_py.tools.read import tool_read
from pi_py.tools.router import run_tool_shortcut
from pi_py.tools.write import tool_write


def test_write_then_read(tmp_path: Path) -> None:
    result = tool_write(tmp_path, "a.txt", "hello")
    assert "wrote" in result
    assert tool_read(tmp_path, "a.txt") == "hello"


def test_safe_path_blocks_escape(tmp_path: Path) -> None:
    try:
        tool_read(tmp_path, "../outside.txt")
        assert False, "expected ValueError"
    except ValueError as exc:
        assert "path escapes cwd" in str(exc)


def test_bash_success(tmp_path: Path) -> None:
    output = tool_bash(tmp_path, "echo hi")
    assert output.strip() == "hi"


def test_run_tool_shortcut_read_and_write(tmp_path: Path) -> None:
    write_result = run_tool_shortcut(tmp_path, "/write x.txt hello")
    assert write_result and "wrote" in write_result
    read_result = run_tool_shortcut(tmp_path, "/read x.txt")
    assert read_result == "hello"


def test_run_tool_shortcut_time(tmp_path: Path) -> None:
    output = run_tool_shortcut(tmp_path, "/time")
    assert output is not None
    assert "T" in output
