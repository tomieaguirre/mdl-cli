from __future__ import annotations

from mdl.core.options import Options, RunOptions
from mdl.services.download_service import run_smoke


def handle_smoke(opts: Options, run_opts: RunOptions) -> int:
    return run_smoke(opts, run_opts)
