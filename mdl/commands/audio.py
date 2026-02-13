from __future__ import annotations

from mdl.core.options import Options, RunOptions
from mdl.services.download_service import run_audio_download


def handle_audio(opts: Options, run_opts: RunOptions) -> int:
    return run_audio_download(opts, run_opts)
