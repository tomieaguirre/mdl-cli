from __future__ import annotations

from pathlib import Path

import pytest

import mdl.core.resolve as resolve


def test_resolve_safe_preset_sets_internal_throttling(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(preset="safe", cookies="none", out_dir="/tmp/safe-out")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options(command="audio"))

    assert run.preset == "safe"
    assert run.limit_rate == str(resolve.Defaults.limit_rate)
    assert run.sleep_min == int(resolve.Defaults.sleep_min)
    assert run.sleep_max == int(resolve.Defaults.sleep_max)
    assert run.out_dir == Path("/tmp/safe-out").resolve()


def test_resolve_fast_preset_disables_internal_throttling(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(preset="fast", cookies="none", out_dir="/tmp/fast-out")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options(command="video"))

    assert run.preset == "fast"
    assert run.limit_rate is None
    assert run.sleep_min is None
    assert run.sleep_max is None
    assert run.out_dir == Path("/tmp/fast-out").resolve()


def test_resolve_unknown_preset_falls_back_to_safe(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(preset="unknown", cookies="none")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options())

    assert run.preset == "safe"
    assert run.limit_rate == str(resolve.Defaults.limit_rate)
    assert run.sleep_min == int(resolve.Defaults.sleep_min)
    assert run.sleep_max == int(resolve.Defaults.sleep_max)


def test_resolve_none_cookies_disables_cookies_from(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(cookies="none")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options())

    assert run.cookies_from is None


def test_resolve_browser_cookies_enables_cookies_from(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(cookies="BrAvE")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options())

    assert run.cookies_from == "brave"


def test_resolve_normalizes_formats_and_cover(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(cover=1, audio_format="OPUS", video_format="MKV")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options())

    assert run.cover is True
    assert run.audio_format == "opus"
    assert run.video_format == "mkv"


def test_resolve_raises_when_safe_sleep_values_are_invalid(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(preset="safe")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)
    monkeypatch.setattr(resolve.Defaults, "sleep_min", 0)
    monkeypatch.setattr(resolve.Defaults, "sleep_max", 10)

    with pytest.raises(SystemExit, match="internal sleep settings are invalid"):
        resolve.resolve_run_options(make_options())


def test_resolve_raises_when_safe_sleep_min_is_greater_than_max(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config(preset="safe")
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)
    monkeypatch.setattr(resolve.Defaults, "sleep_min", 20)
    monkeypatch.setattr(resolve.Defaults, "sleep_max", 10)

    with pytest.raises(SystemExit, match="sleep-min must be <= sleep-max"):
        resolve.resolve_run_options(make_options())


def test_resolve_keeps_valid_playlist_mode_from_cli(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config()
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options(playlist_mode="flat"))

    assert run.playlist_mode == "flat"


def test_resolve_falls_back_to_auto_on_invalid_playlist_mode(monkeypatch, make_options, make_app_config) -> None:
    cfg = make_app_config()
    monkeypatch.setattr(resolve, "load_config", lambda: cfg)

    run = resolve.resolve_run_options(make_options(playlist_mode="weird"))

    assert run.playlist_mode == "auto"
