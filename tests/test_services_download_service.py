from __future__ import annotations

import pytest

import mdl.services.download_service as svc


def test_require_url_raises_when_missing(make_options) -> None:
    with pytest.raises(SystemExit, match="audio requires URL"):
        svc.require_url(make_options(command="audio", url=None))


def test_run_or_print_prints_and_does_not_execute_when_print_enabled(
    monkeypatch,
    make_options,
) -> None:
    printed: list[list[str]] = []
    monkeypatch.setattr(svc, "print_command", lambda cmd: printed.append(cmd))
    monkeypatch.setattr(
        svc,
        "run_command",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("unexpected run_command call")),
    )

    rc = svc._run_or_print(make_options(print_cmd=True), ["yt-dlp", "https://example.com"])

    assert rc == 0
    assert printed == [["yt-dlp", "https://example.com"]]


def test_run_audio_download_builds_command_and_passes_ffmpeg_requirement(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    calls: dict[str, object] = {}

    monkeypatch.setattr(
        svc,
        "build_audio_command",
        lambda url, run_opts: ["audio-cmd", url, run_opts.audio_format],
    )

    def fake_run_or_print(opts, cmd, *, needs_ffmpeg):
        calls["opts"] = opts
        calls["cmd"] = cmd
        calls["needs_ffmpeg"] = needs_ffmpeg
        return 7

    monkeypatch.setattr(svc, "_run_or_print", fake_run_or_print)

    opts = make_options(command="audio", url="https://example.com")
    run_opts = make_run_options(cover=True, audio_format="opus")
    rc = svc.run_audio_download(opts, run_opts)

    assert rc == 7
    assert calls["cmd"] == ["audio-cmd", "https://example.com", "opus"]
    assert calls["needs_ffmpeg"] is True


def test_run_video_download_builds_command_and_passes_ffmpeg_requirement(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(
        svc,
        "build_video_command",
        lambda url, run_opts: ["video-cmd", url, run_opts.video_format],
    )

    def fake_run_or_print(opts, cmd, *, needs_ffmpeg):
        calls["cmd"] = cmd
        calls["needs_ffmpeg"] = needs_ffmpeg
        return 9

    monkeypatch.setattr(svc, "_run_or_print", fake_run_or_print)

    opts = make_options(command="video", url="https://example.com")
    run_opts = make_run_options(cover=False, video_format="mkv")
    rc = svc.run_video_download(opts, run_opts)

    assert rc == 9
    assert calls["cmd"] == ["video-cmd", "https://example.com", "mkv"]
    assert calls["needs_ffmpeg"] is False


def test_run_info_builds_info_command_without_ffmpeg_flag(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(svc, "build_info_command", lambda url, run_opts: ["info-cmd", url])

    def fake_run_or_print(opts, cmd, *, needs_ffmpeg=False):
        calls["cmd"] = cmd
        calls["needs_ffmpeg"] = needs_ffmpeg
        return 3

    monkeypatch.setattr(svc, "_run_or_print", fake_run_or_print)

    opts = make_options(command="info", url="https://example.com")
    rc = svc.run_info(opts, make_run_options())

    assert rc == 3
    assert calls["cmd"] == ["info-cmd", "https://example.com"]
    assert calls["needs_ffmpeg"] is False


def test_run_smoke_audio_print_mode_uses_smoke_audio_url(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    printed: list[list[str]] = []
    monkeypatch.setattr(svc, "build_audio_command", lambda url, run_opts: ["audio-smoke", url])
    monkeypatch.setattr(
        svc,
        "run_command",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("unexpected run_command call")),
    )
    monkeypatch.setattr(svc, "print_command", lambda cmd: printed.append(cmd))

    opts = make_options(command="smoke", smoke_kind="audio", print_cmd=True, url=None)
    rc = svc.run_smoke(opts, make_run_options())

    assert rc == 0
    assert printed == [["audio-smoke", svc.SMOKE_AUDIO_URL]]


def test_run_smoke_video_executes_with_cover_driven_ffmpeg_requirement(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    calls: dict[str, object] = {}
    monkeypatch.setattr(svc, "build_video_command", lambda url, run_opts: ["video-smoke", url])
    monkeypatch.setattr(svc, "print_command", lambda cmd: (_ for _ in ()).throw(AssertionError("unexpected print")))

    def fake_run_command(cmd, *, needs_ffmpeg):
        calls["cmd"] = cmd
        calls["needs_ffmpeg"] = needs_ffmpeg
        return 5

    monkeypatch.setattr(svc, "run_command", fake_run_command)

    opts = make_options(command="smoke", smoke_kind="video", print_cmd=False, url=None)
    rc = svc.run_smoke(opts, make_run_options(cover=True))

    assert rc == 5
    assert calls["cmd"] == ["video-smoke", svc.SMOKE_VIDEO_URL]
    assert calls["needs_ffmpeg"] is True


def test_run_smoke_raises_for_unknown_kind(make_options, make_run_options) -> None:
    opts = make_options(command="smoke", smoke_kind="other", url=None)

    with pytest.raises(SystemExit, match="Unknown smoke kind"):
        svc.run_smoke(opts, make_run_options())
