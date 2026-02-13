from __future__ import annotations

from typing import List

from mdl.builders.yt_dlp_common import base_yt_dlp_args
from mdl.core.config import Defaults
from mdl.core.options import RunOptions
from mdl.core.playlist import is_playlist_url


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
        cmd += ["--embed-thumbnail"]

    # Robustness
    cmd += ["--ignore-errors", "--continue", "--no-overwrites"]

    cmd += ["-o", out_template, url]
    return cmd
