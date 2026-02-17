from __future__ import annotations

from urllib.parse import parse_qs, urlparse

def is_playlist_url(url: str) -> bool:
    """
    Best-effort heuristic used only for output templates.
    yt-dlp remains the source of truth for what gets downloaded.
    """
    return "list=" in url


def detect_playlist_layout(url: str) -> str:
    """
    Return the playlist output layout:
    - "album": artist/channel folder + playlist folder
    - "flat": single playlist folder

    Rules:
    - Non-playlist URLs => "flat" (layout is irrelevant for singles).
    - YouTube Music album list IDs typically start with "OLAK".
    """
    if not is_playlist_url(url):
        return "flat"

    try:
        query = parse_qs(urlparse(url).query)
        list_ids = query.get("list", [])
    except Exception:
        list_ids = []

    list_id = str(list_ids[0]).strip() if list_ids else ""
    if list_id.upper().startswith("OLAK"):
        return "album"
    return "flat"
