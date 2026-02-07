from __future__ import annotations

from pathlib import Path

from mdl.config import Defaults
from mdl.config_store import load_config
from mdl.options import Options, RunOptions


def resolve_run_options(opts: Options) -> RunOptions:
    """
    Resolve runtime options from persisted config + Defaults.

    Note:
    - We intentionally do NOT expose rate/sleep/js runtime/remote components to the user.
      Presets control internal throttling.
    """
    cfg = load_config()

    # out_dir is only meaningful for downloads; info/settings may not provide it.
    out_dir = (opts.out or Defaults.out_dir)
    out_dir = Path(out_dir).expanduser()

    preset = str(cfg.preset).strip().lower()

    # Cookies: "none" disables cookies integration
    cookies = str(cfg.cookies).strip().lower()
    cookies_from = None if cookies == "none" else cookies

    # Preset -> internal throttling (not user-visible)
    if preset == "safe":
        limit_rate = str(Defaults.limit_rate)
        sleep_min = int(Defaults.sleep_min)
        sleep_max = int(Defaults.sleep_max)
    elif preset == "fast":
        limit_rate = None
        sleep_min = None
        sleep_max = None
    else:
        # Defensive fallback: treat unknown preset as safe
        preset = "safe"
        limit_rate = str(Defaults.limit_rate)
        sleep_min = int(Defaults.sleep_min)
        sleep_max = int(Defaults.sleep_max)

    # Defensive sanity checks (even though user can't set these via CLI)
    if preset == "safe":
        if sleep_min is None or sleep_max is None or sleep_min <= 0 or sleep_max <= 0:
            raise SystemExit("[mdl] ERROR: internal sleep settings are invalid.")
        if sleep_min > sleep_max:
            raise SystemExit("[mdl] ERROR: internal sleep-min must be <= sleep-max.")

    return RunOptions(
        out_dir=out_dir,
        preset=preset,
        cookies_from=cookies_from,
        cover=bool(cfg.cover),
        audio_format=str(cfg.audio_format).strip().lower(),
        video_format=str(cfg.video_format).strip().lower(),
        limit_rate=limit_rate,
        sleep_min=sleep_min,
        sleep_max=sleep_max,
    )
