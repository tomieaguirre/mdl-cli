from __future__ import annotations

from mdl.builders.yt_dlp_common import base_yt_dlp_args


def test_base_yt_dlp_args_includes_cookies_rate_and_sleep(make_run_options) -> None:
    opts = make_run_options(
        cookies_from="chrome",
        limit_rate="1M",
        sleep_min=5,
        sleep_max=15,
    )

    args = base_yt_dlp_args(opts)

    assert args == [
        "--cookies-from-browser",
        "chrome",
        "--limit-rate",
        "1M",
        "--sleep-interval",
        "5",
        "--max-sleep-interval",
        "15",
    ]


def test_base_yt_dlp_args_omits_everything_when_unset(make_run_options) -> None:
    args = base_yt_dlp_args(make_run_options())
    assert args == []


def test_base_yt_dlp_args_omits_sleep_when_only_one_boundary_is_set(make_run_options) -> None:
    args = base_yt_dlp_args(make_run_options(sleep_min=5, sleep_max=None))
    assert "--sleep-interval" not in args
    assert "--max-sleep-interval" not in args
