from __future__ import annotations

from mdl.core.options import Options, RunOptions
from mdl.services.download_service import run_info


def handle_info(opts: Options, run_opts: RunOptions) -> int:
    return run_info(opts, run_opts)
