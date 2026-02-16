from __future__ import annotations

import mdl.commands.audio as cmd_audio
import mdl.commands.video as cmd_video
import mdl.commands.info as cmd_info
import mdl.commands.smoke as cmd_smoke


def test_handle_audio_delegates_to_service(monkeypatch, make_options, make_run_options) -> None:
    monkeypatch.setattr(cmd_audio, "run_audio_download", lambda opts, run_opts: 11)
    assert cmd_audio.handle_audio(make_options(command="audio"), make_run_options()) == 11


def test_handle_video_delegates_to_service(monkeypatch, make_options, make_run_options) -> None:
    monkeypatch.setattr(cmd_video, "run_video_download", lambda opts, run_opts: 12)
    assert cmd_video.handle_video(make_options(command="video"), make_run_options()) == 12


def test_handle_info_delegates_to_service(monkeypatch, make_options, make_run_options) -> None:
    monkeypatch.setattr(cmd_info, "run_info", lambda opts, run_opts: 13)
    assert cmd_info.handle_info(make_options(command="info"), make_run_options()) == 13


def test_handle_smoke_delegates_to_service(monkeypatch, make_options, make_run_options) -> None:
    monkeypatch.setattr(cmd_smoke, "run_smoke", lambda opts, run_opts: 14)
    assert cmd_smoke.handle_smoke(make_options(command="smoke"), make_run_options()) == 14
