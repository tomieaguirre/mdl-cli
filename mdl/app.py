from __future__ import annotations

import argparse
from typing import Callable, Dict

from mdl.commands.audio import handle_audio
from mdl.commands.video import handle_video
from mdl.commands.info import handle_info
from mdl.commands.smoke import handle_smoke
from mdl.commands.settings import SETTINGS_COMMANDS, handle_settings
from mdl.core.options import Options
from mdl.core.resolve import resolve_run_options


# Handlers that require RunOptions
_RUN_HANDLERS: Dict[str, Callable] = {
    "info": handle_info,
    "smoke": handle_smoke,
    "audio": handle_audio,
    "video": handle_video,
}


def run_app(args: argparse.Namespace) -> int:
    """
    Application entrypoint (routing/orchestration).

    Responsibilities:
    - Convert argparse Namespace -> Options DTO
    - Handle settings commands (no yt-dlp execution)
    - Resolve RunOptions (config + defaults)
    - Dispatch to the correct command handler
    """
    opts = Options.from_namespace(args)

    # Settings commands: no runtime resolution needed
    if opts.command in SETTINGS_COMMANDS:
        return handle_settings(opts)

    # Resolve runtime options (config + defaults) for commands that invoke yt-dlp
    run_opts = resolve_run_options(opts)

    handler = _RUN_HANDLERS.get(opts.command)
    if handler is None:
        raise SystemExit(f"[mdl] ERROR: Unknown command '{opts.command}'.")

    return handler(opts, run_opts)
