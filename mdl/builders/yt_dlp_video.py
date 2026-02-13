from __future__ import annotations

from typing import List

from mdl.builders.yt_dlp_common import base_yt_dlp_args
from mdl.core.config import Defaults
from mdl.core.options import RunOptions
from mdl.core.playlist import is_playlist_url


def build_video_command(url: str, opts: RunOptions) -> List[str]:
    """
    Build the yt-dlp command for best-quality video.

    Strategy:
    - Always pick best video + best audio (no forced downgrade).
    - Remux to the configured container (mp4/mkv) without re-encoding.
    """
    tpl = Defaults.video_playlist_tpl if is_playlist_url(url) else Defaults.video_single_tpl
    out_template = str(opts.out_dir / tpl)

    cmd: List[str] = ["yt-dlp"]
    cmd += base_yt_dlp_args(opts)

    # Best quality selection (avoid forcing container here)
    cmd += ["-f", "bv*+ba/b"]

    # Remux to the user-chosen container (safe subset: mp4|mkv)
    cmd += ["--remux-video", opts.video_format]

    # Cover behavior (optional)
    if opts.cover:
        cmd += ["--write-thumbnail", "--embed-thumbnail"]

    # Robustness
    cmd += ["--ignore-errors", "--continue", "--no-overwrites"]

    cmd += ["-o", out_template, url]
    return cmd
