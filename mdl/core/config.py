from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re


def _xdg_music_dir() -> Path:
    """
    Best-effort: read XDG user dirs to find the real Music folder.
    Falls back to ~/Music.
    """
    cfg = Path.home() / ".config" / "user-dirs.dirs"
    if cfg.exists():
        txt = cfg.read_text(encoding="utf-8", errors="ignore")

        # Typical line: XDG_MUSIC_DIR="$HOME/Music"
        m = re.search(r'^XDG_MUSIC_DIR=(?P<q>["\'])(?P<val>.*?)(?P=q)\s*$', txt, re.MULTILINE)
        if m:
            val = m.group("val").strip()

            # Support $HOME and ${HOME}
            home = str(Path.home())
            val = val.replace("$HOME", home).replace("${HOME}", home)

            # Expand any remaining env vars
            val = os.path.expandvars(val)

            return Path(val).expanduser()

    return Path.home() / "Music"


@dataclass(frozen=True)
class Defaults:
    # Output
    out_dir: Path = _xdg_music_dir() / "mdl"

    # Networking behavior (safe preset)
    limit_rate: str = "1M"
    sleep_min: int = 5
    sleep_max: int = 15

    # Output templates
    audio_single_tpl: str = "%(artist|uploader)s/%(title)s.%(ext)s"
    audio_playlist_tpl: str = "%(artist|uploader)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s"
    video_single_tpl: str = "%(uploader|channel)s/%(title)s.%(ext)s"
    video_playlist_tpl: str = "%(uploader|channel)s/%(playlist_title)s/%(playlist_index)02d - %(title)s.%(ext)s"
