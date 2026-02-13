from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from mdl import __version__
from mdl.core.config import Defaults
from mdl.app import run_app


def _add_download_flags(p: argparse.ArgumentParser) -> None:
    """
    Flags for download commands (audio/video).
    Intentionally minimal: users should not tune rate/sleep/etc.
    Presets handle that internally.
    """
    p.add_argument("url", metavar="URL", help="Target URL (single item or playlist).")

    p.add_argument(
        "--out",
        metavar="DIR",
        type=Path,
        default=Defaults.out_dir,
        help=f"Output base directory (default: {Defaults.out_dir}).",
    )


def _add_setting_value_arg(p: argparse.ArgumentParser, *, name: str, metavar: str = "VALUE") -> None:
    """
    Adds an optional positional VALUE for setting commands:
    - `mdl <setting>` shows the current value.
    - `mdl <setting> <VALUE>` sets a new value.
    """
    p.add_argument(name, nargs="?", default=None, metavar=metavar)


def _add_print_flag(p: argparse.ArgumentParser) -> None:
    """
    Per-command print flag.
    This makes `--print` valid AFTER the subcommand:
      mdl audio URL --print
    """
    p.add_argument(
        "--print",
        action="store_true",
        help="Print the final yt-dlp command and exit (no execution).",
    )


def build_parser() -> argparse.ArgumentParser:
    """
    CLI definition only. All business logic lives in mdl.app / core / commands.
    """
    parser = argparse.ArgumentParser(
        prog="mdl",
        description="mdl-cli: a human-friendly wrapper around yt-dlp.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
        epilog=(
            "Examples:\n"
            "  mdl audio URL --print\n"
            "  mdl video URL --print\n"
            "  mdl info URL --print\n"
            "  mdl smoke audio\n"
            "  mdl smoke video\n"
            "  mdl audio URL --out ~/Music/mdl\n"
            "\n"
            "Settings:\n"
            "  mdl preset\n"
            "  mdl preset fast\n"
            "  mdl preset --list\n"
            "  mdl cookies brave\n"
            "  mdl cover on\n"
            "  mdl audio-format opus\n"
            "  mdl video-format mkv\n"
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"mdl {__version__}",
        help="Show program version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Downloads
    p_audio = subparsers.add_parser("audio", help="Download best-quality audio.")
    _add_download_flags(p_audio)
    _add_print_flag(p_audio)

    p_video = subparsers.add_parser("video", help="Download best-quality video.")
    _add_download_flags(p_video)
    _add_print_flag(p_video)

    # Info
    p_info = subparsers.add_parser("info", help="Show available formats for a URL (yt-dlp -F).")
    p_info.add_argument("url", metavar="URL", help="Target URL to inspect (no download).")
    _add_print_flag(p_info)

    # Smoke
    p_smoke = subparsers.add_parser("smoke", help="Download a small sample to verify setup.")
    smoke_sub = p_smoke.add_subparsers(dest="smoke_kind", required=True)
    smoke_sub.add_parser("audio", help="Smoke test: audio download.")
    smoke_sub.add_parser("video", help="Smoke test: video download.")
    _add_print_flag(p_smoke)

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
    _add_setting_value_arg(p_audio_fmt, name="value", metavar="opus|m4a|mp3|flac")

    p_video_fmt = subparsers.add_parser("video-format", help="Configure default video container (remux).")
    p_video_fmt.add_argument("--list", action="store_true", help="List allowed values.")
    _add_setting_value_arg(p_video_fmt, name="value", metavar="mp4|mkv")

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()

    # UX: if user runs just `mdl`, show help instead of an error.
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        parser.print_help()
        raise SystemExit(0)

    args = parser.parse_args(argv)
    raise SystemExit(run_app(args))
