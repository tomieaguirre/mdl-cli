from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from mdl.core.options import AppConfig, Options, RunOptions


def _default_test_out_dir() -> str:
    return str((Path.cwd() / "mdl-test-out").resolve())


@pytest.fixture
def make_options() -> Callable[..., Options]:
    def _make(
        *,
        command: str = "audio",
        print_cmd: bool = False,
        url: str | None = "https://example.com",
        playlist_mode: str = "auto",
        smoke_kind: str | None = None,
        list_values: bool = False,
        value: str | None = None,
    ) -> Options:
        return Options(
            command=command,
            print_cmd=print_cmd,
            url=url,
            playlist_mode=playlist_mode,
            smoke_kind=smoke_kind,
            list_values=list_values,
            value=value,
        )

    return _make


@pytest.fixture
def make_run_options() -> Callable[..., RunOptions]:
    def _make(
        *,
        out_dir: str | Path = _default_test_out_dir(),
        preset: str = "safe",
        cookies_from: str | None = None,
        cover: bool = False,
        audio_format: str = "m4a",
        video_format: str = "mp4",
        limit_rate: str | None = None,
        sleep_min: int | None = None,
        sleep_max: int | None = None,
        playlist_mode: str = "auto",
    ) -> RunOptions:
        return RunOptions(
            out_dir=Path(out_dir),
            preset=preset,
            cookies_from=cookies_from,
            cover=cover,
            audio_format=audio_format,
            video_format=video_format,
            limit_rate=limit_rate,
            sleep_min=sleep_min,
            sleep_max=sleep_max,
            playlist_mode=playlist_mode,
        )

    return _make


@pytest.fixture
def make_app_config() -> Callable[..., AppConfig]:
    def _make(
        *,
        preset: str = "safe",
        cookies: str = "none",
        cover: bool = False,
        audio_format: str = "m4a",
        video_format: str = "mp4",
        out_dir: str = _default_test_out_dir(),
    ) -> AppConfig:
        return AppConfig(
            preset=preset,
            cookies=cookies,
            cover=cover,
            audio_format=audio_format,
            video_format=video_format,
            out_dir=out_dir,
        )

    return _make
