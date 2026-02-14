from __future__ import annotations

import sys

from mdl.core.config_store import (
    describe_config_value,
    list_allowed_values,
    load_config,
    save_config,
    set_config_value,
    SETTINGS_COMMANDS,
)
from mdl.core.options import Options



def _handle_setting(cmd: str, value: str | None, list_flag: bool) -> int:
    """
    Settings UX:
    - `mdl <cmd>`: show current value
    - `mdl <cmd> <value>`: set value, persist, print confirmation
    - `mdl <cmd> --list`: list allowed values
    """
    if cmd not in SETTINGS_COMMANDS:
        raise SystemExit(f"[mdl] ERROR: unknown settings command '{cmd}'.")

    if list_flag and cmd != "out":
        values = list_allowed_values(cmd)
        print(f"[mdl] {cmd} allowed: {', '.join(values)}")
        return 0

    cfg = load_config()

    if value is None:
        current = describe_config_value(cfg, cmd)
        print(f"[mdl] {cmd}: {current}")
        return 0

    if cmd == "out" and not str(value).strip():
        raise SystemExit("[mdl] ERROR: out requires a PATH")

    cfg2 = set_config_value(cfg, cmd, value)
    save_config(cfg2)
    current = describe_config_value(cfg2, cmd)
    print(f"[mdl] {cmd}: {current}")
    return 0


def handle_settings(opts: Options) -> int:
    # `--print` makes sense for yt-dlp commands; settings don't execute anything.
    if opts.print_cmd:
        print("[mdl] NOTE: --print is ignored for settings commands.", file=sys.stderr)
    return _handle_setting(opts.command, opts.value, opts.list_values)
