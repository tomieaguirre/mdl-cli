from __future__ import annotations

from mdl.builders.yt_dlp_audio import build_audio_command
from mdl.builders.yt_dlp_video import build_video_command
from mdl.builders.yt_dlp_info import build_info_command
from mdl.core.options import Options, RunOptions
from mdl.infra.runner import print_command, run_command


# Deterministic smoke target.
# Used for both audio and video smoke tests to verify full download pipeline.
SMOKE_URL = "https://www.youtube.com/watch?v=dWRCooFKk3c"

def require_url(opts: Options) -> str:
    if not opts.url:
        cmd = opts.command or "command"
        raise SystemExit(f"[mdl] ERROR: {cmd} requires URL. Try: mdl {cmd} -h")
    return opts.url


def _run_or_print(opts: Options, cmd: list[str], *, needs_ffmpeg: bool = False) -> int:
    if opts.print_cmd:
        print_command(cmd)
        return 0
    return run_command(cmd, needs_ffmpeg=needs_ffmpeg)


def run_audio_download(opts: Options, run_opts: RunOptions) -> int:
    url = require_url(opts)
    cmd = build_audio_command(url, run_opts)
    needs_ffmpeg = run_opts.cover
    return _run_or_print(opts, cmd, needs_ffmpeg=needs_ffmpeg)


def run_video_download(opts: Options, run_opts: RunOptions) -> int:
    url = require_url(opts)
    cmd = build_video_command(url, run_opts)
    needs_ffmpeg = run_opts.cover
    return _run_or_print(opts, cmd, needs_ffmpeg=needs_ffmpeg)


def run_info(opts: Options, run_opts: RunOptions) -> int:
    url = require_url(opts)
    cmd = build_info_command(url, run_opts)
    return _run_or_print(opts, cmd)


def run_smoke(opts: Options, run_opts: RunOptions) -> int:
    if opts.smoke_kind == "audio":
        cmd = build_audio_command(SMOKE_URL, run_opts)
    elif opts.smoke_kind == "video":
        cmd = build_video_command(SMOKE_URL, run_opts)
    else:
        raise SystemExit("[mdl] ERROR: Unknown smoke kind (expected: audio|video).")

    if opts.print_cmd:
        print_command(cmd)
        return 0

    return run_command(cmd, needs_ffmpeg=run_opts.cover)
