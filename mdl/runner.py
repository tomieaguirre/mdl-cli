from __future__ import annotations

import shlex
import subprocess
import sys
from shutil import which
from typing import List, Optional


def printable_cmd(cmd: List[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def print_command(cmd: List[str]) -> None:
    print(f"[mdl] exec: {printable_cmd(cmd)}")


def _command_exists(name: str) -> bool:
    return which(name) is not None


def run_command(cmd: List[str], *, needs_ffmpeg: bool = False) -> int:
    """
    Execute the assembled command.

    - Always prints the final command for transparency.
    - Returns the subprocess exit code.
    - Provides user-friendly errors for missing dependencies.
    """
    print_command(cmd)

    if not _command_exists("yt-dlp"):
        print(
            "[mdl] ERROR: yt-dlp not found in PATH.\n"
            "[mdl]        Install it (recommended): pipx install yt-dlp",
            file=sys.stderr,
        )
        return 127

    if needs_ffmpeg and not _command_exists("ffmpeg"):
        print(
            "[mdl] ERROR: ffmpeg not found in PATH.\n"
            "[mdl]        Install it (Ubuntu/Debian): sudo apt install ffmpeg",
            file=sys.stderr,
        )
        return 127

    try:
        proc = subprocess.run(cmd, check=False)
        return int(proc.returncode)
    except KeyboardInterrupt:
        print("\n[mdl] cancelled by user", file=sys.stderr)
        return 130
    except OSError as e:
        print(f"[mdl] ERROR: failed to execute command: {e}", file=sys.stderr)
        return 1
