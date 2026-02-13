from __future__ import annotations


def is_playlist_url(url: str) -> bool:
    """
    Best-effort heuristic used only for output templates.
    yt-dlp remains the source of truth for what gets downloaded.
    """
    return "list=" in url
