from __future__ import annotations

from mdl.core.options import Options, RunOptions
from mdl.services.download_service import run_video_download


def handle_video(opts: Options, run_opts: RunOptions) -> int:
    return run_video_download(opts, run_opts)
