from __future__ import annotations

from typing import List

from mdl.config import Defaults
from mdl.options import RunOptions
from mdl.playlist import is_playlist_url
from mdl.builders.common import base_yt_dlp_args


def build_audio_command(url: str, opts: RunOptions) -> List[str]:
    """Build the yt-dlp command for best-quality audio downloads."""
    tpl = Defaults.audio_playlist_tpl if is_playlist_url(url) else Defaults.audio_single_tpl
    out_template = str(opts.out_dir / tpl)

    cmd: List[str] = ["yt-dlp"]
    cmd += base_yt_dlp_args(opts)

    cmd += ["-f", "bestaudio/best"]
    cmd += ["-x", "--audio-format", opts.audio_format]

    # Metadata (no quality impact)
    cmd += ["--add-metadata", "--embed-metadata"]

    # Cover behavior (best-effort; actual fallback strategy is handled later)
    if opts.cover:
        cmd += ["--write-thumbnail", "--embed-thumbnail"]

    # Robustness
    cmd += ["--ignore-errors", "--continue", "--no-overwrites"]

    cmd += ["-o", out_template, url]
    return cmd
