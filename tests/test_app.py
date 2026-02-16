from __future__ import annotations

from argparse import Namespace

import pytest

import mdl.app as app


def test_run_app_routes_settings_without_resolving_runtime(
    monkeypatch,
    make_options,
) -> None:
    opts = make_options(command="preset")
    monkeypatch.setattr(app.Options, "from_namespace", staticmethod(lambda ns: opts))
    monkeypatch.setattr(app, "handle_settings", lambda x: 21)
    monkeypatch.setattr(
        app,
        "resolve_run_options",
        lambda x: (_ for _ in ()).throw(AssertionError("resolve_run_options should not be called")),
    )

    rc = app.run_app(Namespace())

    assert rc == 21


def test_run_app_routes_config_without_resolving_runtime(
    monkeypatch,
    make_options,
) -> None:
    opts = make_options(command="config")
    monkeypatch.setattr(app.Options, "from_namespace", staticmethod(lambda ns: opts))
    monkeypatch.setattr(app, "handle_settings", lambda x: 31)
    monkeypatch.setattr(
        app,
        "resolve_run_options",
        lambda x: (_ for _ in ()).throw(AssertionError("resolve_run_options should not be called")),
    )

    rc = app.run_app(Namespace())

    assert rc == 31


def test_run_app_routes_runtime_command_with_resolved_options(
    monkeypatch,
    make_options,
    make_run_options,
) -> None:
    opts = make_options(command="audio")
    run_opts = make_run_options()
    calls: dict[str, object] = {}

    monkeypatch.setattr(app.Options, "from_namespace", staticmethod(lambda ns: opts))
    monkeypatch.setattr(app, "resolve_run_options", lambda x: run_opts)

    def fake_handler(got_opts, got_run_opts):
        calls["opts"] = got_opts
        calls["run_opts"] = got_run_opts
        return 22

    monkeypatch.setitem(app._RUN_HANDLERS, "audio", fake_handler)

    rc = app.run_app(Namespace())

    assert rc == 22
    assert calls["opts"] == opts
    assert calls["run_opts"] == run_opts


def test_run_app_raises_for_unknown_runtime_command(monkeypatch, make_options, make_run_options) -> None:
    opts = make_options(command="unknown-command")
    monkeypatch.setattr(app.Options, "from_namespace", staticmethod(lambda ns: opts))
    monkeypatch.setattr(app, "resolve_run_options", lambda x: make_run_options())

    with pytest.raises(SystemExit, match="Unknown command 'unknown-command'"):
        app.run_app(Namespace())
