from __future__ import annotations

import shutil
import shlex
import subprocess
import sys
from typing import List


def _command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def printable_cmd(cmd: List[str]) -> str:
    return " ".join(shlex.quote(s) for s in cmd)


def print_command(cmd: List[str]) -> None:
    print(f"[mdl] exec: {printable_cmd(cmd)}")


def _check_dependencies(*, needs_ffmpeg: bool) -> int:
    if not _command_exists("yt-dlp"):
        print("[mdl] ERROR: yt-dlp not found in PATH.", file=sys.stderr)
        print("[mdl]        Install it (recommended): pipx install yt-dlp", file=sys.stderr)
        print("[mdl]        Or ensure it is available in your PATH.", file=sys.stderr)
        return 127

    if needs_ffmpeg and not _command_exists("ffmpeg"):
        print("[mdl] ERROR: ffmpeg not found in PATH.", file=sys.stderr)
        print("[mdl]        Install it (Ubuntu/Debian): sudo apt install ffmpeg", file=sys.stderr)
        print("[mdl]        Or ensure it is available in your PATH.", file=sys.stderr)
        return 127

    return 0


def run_command(cmd: List[str], *, needs_ffmpeg: bool = False, print_first: bool = True) -> int:
    """
    Runs the given command, streaming stdout/stderr.
    Returns the subprocess exit code.
    """
    dep_rc = _check_dependencies(needs_ffmpeg=needs_ffmpeg)
    if dep_rc != 0:
        # Keep transparency: still show what would have been executed.
        if print_first:
            print_command(cmd)
        return dep_rc

    if print_first:
        print_command(cmd)

    try:
        p = subprocess.run(cmd)
        return int(p.returncode)
    except KeyboardInterrupt:
        return 130
