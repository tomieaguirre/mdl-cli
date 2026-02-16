from __future__ import annotations

import pytest

import mdl.cli as cli


def test_build_parser_parses_audio_command_with_print_flag() -> None:
    parser = cli.build_parser()

    ns = parser.parse_args(["audio", "https://example.com", "--print"])

    assert ns.command == "audio"
    assert ns.url == "https://example.com"
    assert getattr(ns, "print") is True


def test_build_parser_parses_smoke_subcommand() -> None:
    parser = cli.build_parser()

    ns = parser.parse_args(["smoke", "video", "--print"])

    assert ns.command == "smoke"
    assert ns.smoke_kind == "video"
    assert getattr(ns, "print") is True


def test_build_parser_parses_setting_command_with_value_and_list_flag() -> None:
    parser = cli.build_parser()

    ns = parser.parse_args(["preset", "fast", "--list"])

    assert ns.command == "preset"
    assert ns.value == "fast"
    assert getattr(ns, "list") is True


def test_build_parser_parses_config_command() -> None:
    parser = cli.build_parser()

    ns = parser.parse_args(["config"])

    assert ns.command == "config"


def test_build_parser_rejects_print_flag_for_config() -> None:
    parser = cli.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["config", "--print"])


def test_build_parser_rejects_value_for_config() -> None:
    parser = cli.build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["config", "anything"])


def test_main_without_args_prints_help_and_exits_zero(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        cli.main([])

    captured = capsys.readouterr()
    assert exc.value.code == 0
    assert "usage: mdl" in captured.out


def test_main_delegates_to_run_app_and_exits_with_return_code(monkeypatch) -> None:
    monkeypatch.setattr(cli, "run_app", lambda args: 9)

    with pytest.raises(SystemExit) as exc:
        cli.main(["info", "https://example.com"])

    assert exc.value.code == 9
