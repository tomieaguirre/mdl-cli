from __future__ import annotations

from typing import List

from mdl.options import RunOptions


def base_yt_dlp_args(opts: RunOptions) -> List[str]:
    """Flags shared across all yt-dlp invocations."""
    args: List[str] = []

    if opts.cookies_from:
        args += ["--cookies-from-browser", opts.cookies_from]

    # Preset-derived throttling (only set in safe preset)
    if opts.limit_rate:
        args += ["--limit-rate", opts.limit_rate]

    if opts.sleep_min is not None and opts.sleep_max is not None:
        args += [
            "--sleep-interval",
            str(opts.sleep_min),
            "--max-sleep-interval",
            str(opts.sleep_max),
        ]

    return args
