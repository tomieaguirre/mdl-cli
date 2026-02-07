from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, List

from mdl import __version__
from mdl.config import Defaults
from mdl.app import run_app


def _add_download_flags(p: argparse.ArgumentParser) -> None:
    """
    Flags for download commands (audio/video).
    Intentionally minimal: users should not tune rate/sleep/etc. Presets handle that internally.
    """
    p.add_argument("url", help="Target URL (single item or playlist).")

    p.add_argument(
        "--out",
        type=Path,
        default=Defaults.out_dir,
        help=f"Output base directory. Default: {Defaults.out_dir}",
    )


def _add_setting_value_arg(p: argparse.ArgumentParser, *, name: str, metavar: str = "VALUE") -> None:
    """
    Adds an optional positional VALUE for setting commands:
    - `mdl <setting>` shows the current value.
    - `mdl <setting> <VALUE>` sets a new value.
    """
    p.add_argument(name, nargs="?", default=None, metavar=metavar)


def build_parser() -> argparse.ArgumentParser:
    """
    CLI definition only. All business logic lives in mdl.app / resolve / builders.
    """
    parser = argparse.ArgumentParser(
        prog="mdl",
        description="mdl-cli: a human-friendly wrapper around yt-dlp.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"mdl {__version__}",
        help="Show program version and exit.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the final yt-dlp command and exit (no execution).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Downloads
    p_audio = subparsers.add_parser("audio", help="Download best-quality audio.")
    _add_download_flags(p_audio)

    p_video = subparsers.add_parser("video", help="Download best-quality video.")
    _add_download_flags(p_video)

    p_info = subparsers.add_parser("info", help="Show available formats for a URL (yt-dlp -F).")
    p_info.add_argument("url", help="Target URL to inspect (no download).")

    p_smoke = subparsers.add_parser("smoke", help="Download a small sample to verify setup.")
    smoke_sub = p_smoke.add_subparsers(dest="smoke_kind", required=True)
    smoke_sub.add_parser("audio", help="Smoke test: audio download.")
    smoke_sub.add_parser("video", help="Smoke test: video download.")

    # Persistent settings (show on no arg, set on value, list on --list)
    p_cover = subparsers.add_parser("cover", help="Configure cover behavior (thumbnail).")
    p_cover.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_cover, name="value", metavar="on|off")

    p_cookies = subparsers.add_parser("cookies", help="Configure cookies browser (or disable).")
    p_cookies.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_cookies, name="value", metavar="BROWSER|none")

    p_preset = subparsers.add_parser("preset", help="Configure the default preset (safe/fast).")
    p_preset.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_preset, name="value", metavar="safe|fast")

    p_audio_fmt = subparsers.add_parser("audio-format", help="Configure default audio container.")
    p_audio_fmt.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_audio_fmt, name="value", metavar="flac|mp3|opus|m4a")

    p_video_fmt = subparsers.add_parser("video-format", help="Configure default video container (remux).")
    p_video_fmt.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_video_fmt, name="value", metavar="mp4|mkv")

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    raise SystemExit(run_app(args))
