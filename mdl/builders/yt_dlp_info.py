from __future__ import annotations

from typing import List

from mdl.builders.yt_dlp_common import base_yt_dlp_args
from mdl.core.options import RunOptions


def build_info_command(url: str, opts: RunOptions) -> List[str]:
    """
    Build the yt-dlp command to display available formats for a URL.

    Equivalent to: yt-dlp -F URL
    """
    cmd: List[str] = ["yt-dlp"]
    cmd += base_yt_dlp_args(opts)
    cmd += ["-F", url]
    return cmd
