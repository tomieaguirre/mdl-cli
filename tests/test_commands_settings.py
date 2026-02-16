from __future__ import annotations

import json

import pytest

import mdl.commands.settings as settings


def test_handle_setting_lists_allowed_values_for_non_out(monkeypatch, capsys) -> None:
    monkeypatch.setattr(settings, "list_allowed_values", lambda cmd: ["safe", "fast"])

    rc = settings._handle_setting("preset", value=None, list_flag=True)
    captured = capsys.readouterr()

    assert rc == 0
    assert "[mdl] preset allowed: safe, fast" in captured.out


def test_handle_setting_prints_current_value_when_value_not_provided(monkeypatch, capsys, make_app_config) -> None:
    monkeypatch.setattr(settings, "load_config", lambda: make_app_config(preset="fast"))
    monkeypatch.setattr(settings, "describe_config_value", lambda cfg, cmd: cfg.preset)

    rc = settings._handle_setting("preset", value=None, list_flag=False)
    captured = capsys.readouterr()

    assert rc == 0
    assert "[mdl] preset: fast" in captured.out


def test_handle_setting_config_prints_effective_config_as_json(monkeypatch, capsys, make_app_config) -> None:
    cfg = make_app_config(
        preset="fast",
        cookies="chrome",
        cover=True,
        audio_format="opus",
        video_format="mkv",
        out_dir="/tmp/out",
    )
    monkeypatch.setattr(settings, "load_config", lambda: cfg)

    rc = settings._handle_setting("config", value=None, list_flag=False)
    captured = capsys.readouterr()

    assert rc == 0
    parsed = json.loads(captured.out)
    assert parsed == {
        "preset": "fast",
        "cookies": "chrome",
        "cover": True,
        "audio_format": "opus",
        "video_format": "mkv",
        "out_dir": "/tmp/out",
    }


def test_handle_setting_updates_and_saves_value(monkeypatch, capsys, make_app_config) -> None:
    original = make_app_config(preset="safe")
    updated = make_app_config(preset="fast")
    saved: list[object] = []

    monkeypatch.setattr(settings, "load_config", lambda: original)
    monkeypatch.setattr(settings, "set_config_value", lambda cfg, cmd, value: updated)
    monkeypatch.setattr(settings, "save_config", lambda cfg: saved.append(cfg))
    monkeypatch.setattr(settings, "describe_config_value", lambda cfg, cmd: cfg.preset)

    rc = settings._handle_setting("preset", value="fast", list_flag=False)
    captured = capsys.readouterr()

    assert rc == 0
    assert saved == [updated]
    assert "[mdl] preset: fast" in captured.out


def test_handle_setting_out_rejects_blank_value() -> None:
    with pytest.raises(SystemExit, match="out requires a PATH"):
        settings._handle_setting("out", value="   ", list_flag=False)


def test_handle_setting_raises_for_unknown_command() -> None:
    with pytest.raises(SystemExit, match="unknown settings command"):
        settings._handle_setting("unknown", value=None, list_flag=False)


def test_handle_settings_warns_when_print_flag_is_used(monkeypatch, capsys, make_options) -> None:
    opts = make_options(command="preset", print_cmd=True)
    monkeypatch.setattr(settings, "_handle_setting", lambda cmd, value, list_flag: 0)

    rc = settings.handle_settings(opts)
    captured = capsys.readouterr()

    assert rc == 0
    assert "--print is ignored for settings commands" in captured.err
