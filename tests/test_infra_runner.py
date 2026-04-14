from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from mdl.infra import runner


def test_printable_cmd_quotes_arguments_with_spaces() -> None:
    rendered = runner.printable_cmd(["yt-dlp", "with space"])
    if os.name == "nt":
        assert rendered == 'yt-dlp "with space"'
    else:
        assert rendered == "yt-dlp 'with space'"


def test_check_dependencies_returns_127_when_yt_dlp_is_missing(monkeypatch, capsys) -> None:
    monkeypatch.setattr(runner, "_command_exists", lambda name: False if name == "yt-dlp" else True)

    rc = runner._check_dependencies(needs_ffmpeg=False)
    captured = capsys.readouterr()

    assert rc == 127
    assert "yt-dlp not found in PATH" in captured.err


def test_check_dependencies_returns_127_when_ffmpeg_is_required_and_missing(monkeypatch, capsys) -> None:
    monkeypatch.setattr(runner, "_command_exists", lambda name: name == "yt-dlp")

    rc = runner._check_dependencies(needs_ffmpeg=True)
    captured = capsys.readouterr()

    assert rc == 127
    assert "ffmpeg not found in PATH" in captured.err


def test_run_command_returns_dependency_error_and_still_prints_command(monkeypatch, capsys) -> None:
    monkeypatch.setattr(runner, "_check_dependencies", lambda *, needs_ffmpeg: 127)
    monkeypatch.setattr(runner.subprocess, "run", lambda cmd: (_ for _ in ()).throw(AssertionError("unexpected call")))

    rc = runner.run_command(["yt-dlp", "https://example.com"], print_first=True)
    captured = capsys.readouterr()

    assert rc == 127
    assert "[mdl] exec:" in captured.out


def test_run_command_executes_and_returns_subprocess_code(monkeypatch) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(runner, "_check_dependencies", lambda *, needs_ffmpeg: 0)

    def fake_run(cmd: list[str]):
        calls["cmd"] = cmd
        return SimpleNamespace(returncode=42)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    rc = runner.run_command(["yt-dlp", "https://example.com"], print_first=False)

    assert rc == 42
    assert calls["cmd"] == ["yt-dlp", "https://example.com"]


def test_run_command_returns_130_on_keyboard_interrupt(monkeypatch) -> None:
    monkeypatch.setattr(runner, "_check_dependencies", lambda *, needs_ffmpeg: 0)
    monkeypatch.setattr(runner.subprocess, "run", lambda cmd: (_ for _ in ()).throw(KeyboardInterrupt()))

    rc = runner.run_command(["yt-dlp", "https://example.com"], print_first=False)

    assert rc == 130
