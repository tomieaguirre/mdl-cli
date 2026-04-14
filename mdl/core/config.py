from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
import sys


def _expand_path(raw: str) -> Path:
    return Path(os.path.expandvars(raw)).expanduser()


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

            # Expand any remaining env vars and user markers.
            return _expand_path(val)

    return Path.home() / "Music"


def default_music_dir() -> Path:
    """
    Return the best default Music directory for the current platform.
    Linux prefers XDG user-dirs; other platforms default to ~/Music.
    """
    if sys.platform.startswith("linux"):
        return _xdg_music_dir()
    return Path.home() / "Music"


def default_config_dir(app_name: str = "mdl") -> Path:
    """
    Return an OS-appropriate config directory.
    - Linux/Unix: $XDG_CONFIG_HOME/<app> or ~/.config/<app>
    - macOS/iOS: ~/Library/Application Support/<app>
    - Windows: %APPDATA%\\<app> (fallback to %LOCALAPPDATA%\\<app>)
    """
    if sys.platform == "win32":
        base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
        if base:
            return _expand_path(base) / app_name
        return Path.home() / "AppData" / "Roaming" / app_name

    if sys.platform == "darwin" or sys.platform.startswith("ios"):
        return Path.home() / "Library" / "Application Support" / app_name

    xdg_base = os.environ.get("XDG_CONFIG_HOME")
    if xdg_base:
        return _expand_path(xdg_base) / app_name
    return Path.home() / ".config" / app_name


@dataclass(frozen=True)
class Defaults:
    # Output
    out_dir: Path = default_music_dir() / "mdl"

    # Networking behavior (safe preset)
    limit_rate: str = "1M"
    sleep_min: int = 5
    sleep_max: int = 15

    # Output templates
    # Album layout: keep grouping by artist -> album/playlist title.
    audio_single_tpl: str = "%(artists.0|artist|uploader)s/%(title)s.%(ext)s"
    audio_playlist_tpl: str = "%(artists.0|artist|uploader)s/%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s"
    video_playlist_tpl: str = "%(uploader|channel)s/%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s"

    # Flat layout: keep all playlist entries under a single playlist folder.
    audio_playlist_flat_tpl: str = "%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s"
    video_playlist_flat_tpl: str = "%(playlist_title|playlist)s/%(playlist_index)02d - %(title)s.%(ext)s"

    video_single_tpl: str = "%(uploader|channel)s/%(title)s.%(ext)s"
