from __future__ import annotations

from mdl.core.playlist import detect_playlist_layout, is_playlist_url


def test_is_playlist_url_true_when_list_query_present() -> None:
    assert is_playlist_url("https://example.com/watch?v=abc&list=PLxyz") is True


def test_is_playlist_url_false_when_list_query_missing() -> None:
    assert is_playlist_url("https://example.com/watch?v=abc") is False


def test_detect_playlist_layout_detects_album_for_olak_list_ids() -> None:
    url = "https://music.youtube.com/playlist?list=OLAK5uy_test"
    assert detect_playlist_layout(url) == "album"


def test_detect_playlist_layout_defaults_to_flat_for_regular_playlists() -> None:
    url = "https://www.youtube.com/playlist?list=PLabc123"
    assert detect_playlist_layout(url) == "flat"
