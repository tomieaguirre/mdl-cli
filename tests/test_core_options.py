from __future__ import annotations

from argparse import Namespace

from mdl.core.options import Options


def test_from_namespace_maps_all_fields() -> None:
    ns = Namespace(
        command="audio",
        url="https://example.com",
        playlist_mode="flat",
        smoke_kind=None,
        value="opus",
    )
    setattr(ns, "print", True)
    setattr(ns, "list", False)

    opts = Options.from_namespace(ns)

    assert opts == Options(
        command="audio",
        print_cmd=True,
        url="https://example.com",
        playlist_mode="flat",
        smoke_kind=None,
        list_values=False,
        value="opus",
    )


def test_from_namespace_defaults_optional_fields_when_missing() -> None:
    ns = Namespace(command="smoke")
    setattr(ns, "print", False)

    opts = Options.from_namespace(ns)

    assert opts.command == "smoke"
    assert opts.print_cmd is False
    assert opts.url is None
    assert opts.playlist_mode == "auto"
    assert opts.smoke_kind is None
    assert opts.list_values is False
    assert opts.value is None


def test_from_namespace_coerces_present_fields_to_string() -> None:
    ns = Namespace(command=123, url=456, playlist_mode=999, smoke_kind=789, value=101112)
    setattr(ns, "print", False)
    setattr(ns, "list", True)

    opts = Options.from_namespace(ns)

    assert opts.command == "123"
    assert opts.url == "456"
    assert opts.playlist_mode == "999"
    assert opts.smoke_kind == "789"
    assert opts.value == "101112"
    assert opts.list_values is True
