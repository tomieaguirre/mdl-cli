from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Options:
    """
    Raw CLI options (argparse output). Some fields are optional because not all
    subcommands require them.
    """
    command: str
    print_cmd: bool

    # Download/info
    url: Optional[str]

    # Smoke
    smoke_kind: Optional[str]  # "audio" | "video"

    # Settings commands
    list_values: bool          # --list
    value: Optional[str]       # optional positional VALUE for settings

    @staticmethod
    def from_namespace(ns) -> "Options":
        # In cli.py you used --print (dest defaults to "print").
        # We store it internally as print_cmd to avoid using name "print".
        return Options(
            command=str(ns.command),
            print_cmd=bool(getattr(ns, "print", False)),

            url=(str(ns.url) if hasattr(ns, "url") else None),

            smoke_kind=(str(ns.smoke_kind) if hasattr(ns, "smoke_kind") else None),

            list_values=bool(getattr(ns, "list", False)),
            value=(str(ns.value) if hasattr(ns, "value") and ns.value is not None else None),
        )


@dataclass(frozen=True)
class AppConfig:
    """
    Persistent user configuration (Linux V1).
    Values should be normalized (lowercase).
    """
    preset: str               # "safe" | "fast"
    cookies: str              # "none" | "brave" | "chrome" | ...
    cover: bool               # cover behavior enabled
    audio_format: str         # "flac" | "mp3" | "opus" | "m4a"
    video_format: str         # "mp4" | "mkv"
    out_dir: str              # absolute base output path as string


@dataclass(frozen=True)
class RunOptions:
    """
    Resolved runtime options used by builders/runner.
    Combines Defaults + AppConfig + command context.

    Invariants:
    - out_dir is defined (downloads)
    - cookies_from is None when cookies are disabled
    - limit_rate/sleep* are only set in safe preset
    """
    out_dir: Path
    preset: str
    cookies_from: Optional[str]
    cover: bool
    audio_format: str
    video_format: str

    # Internal network throttling derived from preset (not user-exposed)
    limit_rate: Optional[str]
    sleep_min: Optional[int]
    sleep_max: Optional[int]
