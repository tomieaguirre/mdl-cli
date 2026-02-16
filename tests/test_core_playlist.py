from __future__ import annotations

from mdl.core.playlist import is_playlist_url


def test_is_playlist_url_true_when_list_query_present() -> None:
    assert is_playlist_url("https://example.com/watch?v=abc&list=PLxyz") is True


def test_is_playlist_url_false_when_list_query_missing() -> None:
    assert is_playlist_url("https://example.com/watch?v=abc") is False
