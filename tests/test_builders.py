from __future__ import annotations

from pathlib import Path

from mdl.builders.yt_dlp_audio import build_audio_command
from mdl.builders.yt_dlp_video import build_video_command
from mdl.builders.yt_dlp_info import build_info_command
from mdl.core.config import Defaults


def _assert_contains_kv(cmd: list[str], key: str, value: str) -> None:
    assert key in cmd, f"Expected {key} in command: {cmd}"
    idx = cmd.index(key)
    assert idx + 1 < len(cmd), f"Expected value after {key}: {cmd}"
    assert cmd[idx + 1] == value, f"Expected {key} {value}, got {cmd[idx:idx+2]}"


def test_audio_single_with_shared_flags_and_cover_snapshot(make_run_options) -> None:
    url = "https://example.com"
    opts = make_run_options(
        cookies_from="brave",
        cover=True,
        audio_format="opus",
        limit_rate="1M",
        sleep_min=5,
        sleep_max=15,
    )

    cmd = build_audio_command(url, opts)

    assert cmd == [
        "yt-dlp",
        "--cookies-from-browser",
        "brave",
        "--limit-rate",
        "1M",
        "--sleep-interval",
        "5",
        "--max-sleep-interval",
        "15",
        "-f",
        "bestaudio/best",
        "-x",
        "--audio-format",
        "opus",
        "--add-metadata",
        "--embed-metadata",
        "--embed-thumbnail",
        "--ignore-errors",
        "--continue",
        "--no-overwrites",
        "-o",
        str(Path("/tmp/mdl") / Defaults.audio_single_tpl),
        url,
    ]


def test_audio_playlist_uses_playlist_template_and_no_cover_flags(make_run_options) -> None:
    url = "https://example.com/watch?v=abc123&list=PLxyz"
    opts = make_run_options()

    cmd = build_audio_command(url, opts)

    assert cmd[0] == "yt-dlp"
    _assert_contains_kv(cmd, "-f", "bestaudio/best")
    assert "-x" in cmd
    _assert_contains_kv(cmd, "--audio-format", "m4a")
    assert "--add-metadata" in cmd
    assert "--embed-metadata" in cmd
    assert "--ignore-errors" in cmd
    assert "--continue" in cmd
    assert "--no-overwrites" in cmd

    assert "--write-thumbnail" not in cmd
    assert "--embed-thumbnail" not in cmd

    # Template playlist
    _assert_contains_kv(cmd, "-o", str(Path("/tmp/mdl") / Defaults.audio_playlist_tpl))

    assert cmd[-1] == url


def test_video_single_cover_flags_present_only_when_cover_true(make_run_options) -> None:
    url = "https://example.com"
    opts = make_run_options(cover=True, video_format="mkv")

    cmd = build_video_command(url, opts)

    assert cmd[0] == "yt-dlp"
    _assert_contains_kv(cmd, "-f", "bv*+ba/b")
    _assert_contains_kv(cmd, "--remux-video", "mkv")

    # cover ON => flags presentes
    assert "--write-thumbnail" in cmd
    assert "--embed-thumbnail" in cmd

    _assert_contains_kv(cmd, "-o", str(Path("/tmp/mdl") / Defaults.video_single_tpl))
    assert cmd[-1] == url


def test_video_playlist_cover_flags_absent_when_cover_false(make_run_options) -> None:
    url = "https://example.com/watch?v=xyz789&list=PLabc"
    opts = make_run_options(cover=False, video_format="mp4")

    cmd = build_video_command(url, opts)

    assert cmd[0] == "yt-dlp"
    _assert_contains_kv(cmd, "-f", "bv*+ba/b")
    _assert_contains_kv(cmd, "--remux-video", "mp4")

    assert "--write-thumbnail" not in cmd
    assert "--embed-thumbnail" not in cmd

    _assert_contains_kv(cmd, "-o", str(Path("/tmp/mdl") / Defaults.video_playlist_tpl))
    assert cmd[-1] == url


def test_info_command_minimal(make_run_options) -> None:
    url = "https://example.com"
    opts = make_run_options()

    cmd = build_info_command(url, opts)
    assert cmd == ["yt-dlp", "-F", url]


def test_info_command_includes_shared_flags_when_present(make_run_options) -> None:
    url = "https://example.com"
    opts = make_run_options(
        cookies_from="chrome",
        limit_rate="1M",
        sleep_min=5,
        sleep_max=15,
    )

    cmd = build_info_command(url, opts)

    assert cmd[0] == "yt-dlp"
    _assert_contains_kv(cmd, "--cookies-from-browser", "chrome")
    _assert_contains_kv(cmd, "--limit-rate", "1M")
    _assert_contains_kv(cmd, "--sleep-interval", "5")
    _assert_contains_kv(cmd, "--max-sleep-interval", "15")
    assert cmd[-2:] == ["-F", url]
