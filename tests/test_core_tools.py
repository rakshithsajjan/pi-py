from pathlib import Path

from pi_py.core import run_tool_shortcut, tool_bash, tool_read, tool_write


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

