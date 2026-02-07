from __future__ import annotations

import argparse

from mdl.options import Options
from mdl.resolve import resolve_run_options

from mdl.builders.audio import build_audio_command
from mdl.builders.video import build_video_command
from mdl.builders.info import build_info_command
from mdl.runner import run_command, print_command

from mdl.config_store import (
    load_config,
    save_config,
    describe_config_value,
    set_config_value,
    list_allowed_values,
)


_SETTINGS = {"cover", "cookies", "preset", "audio-format", "video-format"}


def _handle_setting(cmd: str, value: str | None, list_flag: bool) -> int:
    """
    Settings UX:
    - `mdl <cmd>`: show current value
    - `mdl <cmd> <value>`: set value, persist, print confirmation
    - `mdl <cmd> --list`: list allowed values
    """
    if list_flag:
        values = list_allowed_values(cmd)
        print(f"[mdl] {cmd} allowed: {', '.join(values)}")
        return 0

    cfg = load_config()

    if value is None:
        current = describe_config_value(cfg, cmd)
        print(f"[mdl] {cmd}: {current}")
        return 0

    cfg2 = set_config_value(cfg, cmd, value)
    save_config(cfg2)
    current = describe_config_value(cfg2, cmd)
    print(f"[mdl] {cmd}: {current}")
    return 0


def _require_url(opts: Options) -> str:
    if not opts.url:
        raise SystemExit("[mdl] ERROR: URL is required for this command.")
    return opts.url


def run_app(args: argparse.Namespace) -> int:
    opts = Options.from_namespace(args)

    # ─────────────────────────────────────────────────────────────
    # Settings commands (no yt-dlp execution)
    # ─────────────────────────────────────────────────────────────
    if opts.command in _SETTINGS:
        if opts.print_cmd:
            print("[mdl] NOTE: --print is ignored for settings commands.")
        return _handle_setting(opts.command, opts.value, opts.list_values)

    # Resolve runtime options (config + defaults)
    run_opts = resolve_run_options(opts)

    # ─────────────────────────────────────────────────────────────
    # info (no download)
    # ─────────────────────────────────────────────────────────────
    if opts.command == "info":
        url = _require_url(opts)
        cmd = build_info_command(url, run_opts)
        if opts.print_cmd:
            print_command(cmd)
            return 0
        return run_command(cmd)

    # ─────────────────────────────────────────────────────────────
    # smoke (stable test downloads)
    # ─────────────────────────────────────────────────────────────
    if opts.command == "smoke":
        if opts.smoke_kind == "audio":
            url = "ytsearch1:creative commons music test"
            cmd = build_audio_command(url, run_opts)
        elif opts.smoke_kind == "video":
            url = "ytsearch1:test video"
            cmd = build_video_command(url, run_opts)
        else:
            raise SystemExit("[mdl] ERROR: Unknown smoke kind (expected: audio|video).")

        if opts.print_cmd:
            print_command(cmd)
            return 0
        return run_command(cmd, needs_ffmpeg=run_opts.cover)

    # ─────────────────────────────────────────────────────────────
    # Downloads
    # ─────────────────────────────────────────────────────────────
    if opts.command == "audio":
        url = _require_url(opts)
        cmd = build_audio_command(url, run_opts)
    elif opts.command == "video":
        url = _require_url(opts)
        cmd = build_video_command(url, run_opts)
    else:
        raise SystemExit("[mdl] ERROR: Unknown command.")

    if opts.print_cmd:
        print_command(cmd)
        return 0

    return run_command(cmd, needs_ffmpeg=run_opts.cover)
