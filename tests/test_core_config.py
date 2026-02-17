from __future__ import annotations

from pathlib import Path

import mdl.core.config as core_config


def test_xdg_music_dir_falls_back_to_home_music_when_config_file_is_missing(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(core_config.Path, "home", staticmethod(lambda: tmp_path))

    result = core_config._xdg_music_dir()

    assert result == tmp_path / "Music"


def test_xdg_music_dir_reads_user_dirs_file_and_expands_home(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(core_config.Path, "home", staticmethod(lambda: tmp_path))
    cfg_file = tmp_path / ".config" / "user-dirs.dirs"
    cfg_file.parent.mkdir(parents=True, exist_ok=True)
    cfg_file.write_text('XDG_MUSIC_DIR="$HOME/MyMusic"\n', encoding="utf-8")

    result = core_config._xdg_music_dir()

    assert result == tmp_path / "MyMusic"


def test_defaults_audio_templates_use_primary_artist_first() -> None:
    assert core_config.Defaults.audio_single_tpl.startswith("%(artists.0|artist|uploader)s/")
    assert core_config.Defaults.audio_playlist_tpl.startswith("%(artists.0|artist|uploader)s/")


def test_defaults_flat_playlist_templates_group_under_playlist_folder() -> None:
    assert core_config.Defaults.audio_playlist_flat_tpl.startswith("%(playlist_title|playlist)s/")
    assert core_config.Defaults.video_playlist_flat_tpl.startswith("%(playlist_title|playlist)s/")
