from __future__ import annotations

import json
from pathlib import Path

import pytest

from mdl.core import config_store


@pytest.fixture
def config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("MDL_CONFIG_DIR", str(tmp_path))
    return tmp_path


def test_load_config_returns_defaults_when_file_is_missing(config_dir: Path) -> None:
    cfg = config_store.load_config()

    assert cfg.preset == "safe"
    assert cfg.cookies == "none"
    assert cfg.cover is False
    assert cfg.audio_format == "m4a"
    assert cfg.video_format == "mp4"
    assert str(Path(cfg.out_dir).expanduser())


def test_load_config_returns_defaults_when_json_is_invalid(config_dir: Path) -> None:
    (config_dir / "config.json").write_text("{this-is:broken", encoding="utf-8")

    cfg = config_store.load_config()

    assert cfg == config_store.default_config()


def test_load_config_normalizes_and_filters_invalid_values(config_dir: Path) -> None:
    payload = {
        "preset": "FAST",
        "cookies": "BrAvE",
        "cover": 1,
        "audio_format": "OPUS",
        "video_format": "MKV",
        "out_dir": "./downloads",
    }
    (config_dir / "config.json").write_text(json.dumps(payload), encoding="utf-8")

    cfg = config_store.load_config()

    assert cfg.preset == "fast"
    assert cfg.cookies == "brave"
    assert cfg.cover is True
    assert cfg.audio_format == "opus"
    assert cfg.video_format == "mkv"
    assert cfg.out_dir == str(Path("./downloads").resolve())


def test_load_config_falls_back_to_defaults_for_invalid_allowed_values(config_dir: Path) -> None:
    payload = {
        "preset": "turbo",
        "cookies": "safari",
        "cover": False,
        "audio_format": "aac",
        "video_format": "avi",
        "out_dir": "",
    }
    (config_dir / "config.json").write_text(json.dumps(payload), encoding="utf-8")

    cfg = config_store.load_config()
    defaults = config_store.default_config()

    assert cfg.preset == defaults.preset
    assert cfg.cookies == defaults.cookies
    assert cfg.audio_format == defaults.audio_format
    assert cfg.video_format == defaults.video_format
    assert cfg.out_dir == defaults.out_dir


def test_save_config_persists_json_file(config_dir: Path, make_app_config) -> None:
    out_dir = str((Path.cwd() / "custom-out").resolve())
    cfg = make_app_config(
        preset="fast",
        cookies="chrome",
        cover=True,
        audio_format="flac",
        video_format="mkv",
        out_dir=out_dir,
    )

    config_store.save_config(cfg)

    raw = (config_dir / "config.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["preset"] == "fast"
    assert data["cookies"] == "chrome"
    assert data["cover"] is True
    assert data["audio_format"] == "flac"
    assert data["video_format"] == "mkv"
    assert data["out_dir"] == out_dir


def test_list_allowed_values_for_known_setting() -> None:
    values = config_store.list_allowed_values("audio-format")
    assert values == ["flac", "mp3", "opus", "m4a"]


def test_settings_commands_includes_config_command() -> None:
    assert "config" in config_store.SETTINGS_COMMANDS


def test_list_allowed_values_raises_for_unknown_setting() -> None:
    with pytest.raises(SystemExit, match="unknown setting"):
        config_store.list_allowed_values("unknown-setting")


def test_describe_config_value_handles_all_supported_settings(make_app_config) -> None:
    out_dir = str((Path.cwd() / "out").resolve())
    cfg = make_app_config(
        preset="fast",
        cookies="firefox",
        cover=True,
        audio_format="opus",
        video_format="mkv",
        out_dir=out_dir,
    )

    assert config_store.describe_config_value(cfg, "cover") == "on"
    assert config_store.describe_config_value(cfg, "cookies") == "firefox"
    assert config_store.describe_config_value(cfg, "preset") == "fast"
    assert config_store.describe_config_value(cfg, "audio-format") == "opus"
    assert config_store.describe_config_value(cfg, "video-format") == "mkv"
    assert config_store.describe_config_value(cfg, "out") == out_dir


@pytest.mark.parametrize(
    ("setting", "value", "expected_attr", "expected_value"),
    [
        ("cover", "on", "cover", True),
        ("cover", "off", "cover", False),
        ("cookies", "chrome", "cookies", "chrome"),
        ("preset", "fast", "preset", "fast"),
        ("audio-format", "mp3", "audio_format", "mp3"),
        ("video-format", "mkv", "video_format", "mkv"),
    ],
)
def test_set_config_value_updates_each_supported_setting(
    setting: str,
    value: str,
    expected_attr: str,
    expected_value: object,
    make_app_config,
) -> None:
    cfg = make_app_config()

    updated = config_store.set_config_value(cfg, setting, value)

    assert getattr(updated, expected_attr) == expected_value


def test_set_config_value_updates_out_with_resolved_path(make_app_config) -> None:
    cfg = make_app_config(out_dir=str((Path.cwd() / "original").resolve()))

    updated = config_store.set_config_value(cfg, "out", "./new-out")

    assert updated.out_dir == str(Path("./new-out").resolve())


def test_config_dir_uses_env_override_with_var_expansion(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MDL_CUSTOM_ROOT", str(tmp_path))
    monkeypatch.setenv("MDL_CONFIG_DIR", "$MDL_CUSTOM_ROOT")

    assert config_store._config_dir() == tmp_path


def test_config_dir_falls_back_to_platform_default_when_env_missing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("MDL_CONFIG_DIR", raising=False)
    expected = tmp_path / "cfg"
    monkeypatch.setattr(config_store, "default_config_dir", lambda _app_name: expected)

    assert config_store._config_dir() == expected


def test_set_config_value_out_rejects_empty_path(make_app_config) -> None:
    with pytest.raises(SystemExit, match="out requires a PATH"):
        config_store.set_config_value(make_app_config(), "out", "   ")


def test_set_config_value_rejects_invalid_choice(make_app_config) -> None:
    with pytest.raises(SystemExit, match="invalid value"):
        config_store.set_config_value(make_app_config(), "preset", "turbo")
