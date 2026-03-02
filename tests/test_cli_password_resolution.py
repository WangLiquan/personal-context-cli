from __future__ import annotations

import argparse
import subprocess

import pytest

from personal_context_cli import cli


def _parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(prog="personal-context")


def test_resolve_password_uses_keychain_on_macos(monkeypatch) -> None:
    monkeypatch.setenv("PCTX_PASSWORD", "")
    monkeypatch.delenv("PCTX_DISABLE_KEYCHAIN", raising=False)
    monkeypatch.setattr("personal_context_cli.cli.sys.platform", "darwin")
    monkeypatch.setattr("personal_context_cli.cli.os.getenv", lambda key, default=None: {"USER": "tester"}.get(key, default))

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="from-keychain\n", stderr="")

    monkeypatch.setattr("personal_context_cli.cli.subprocess.run", fake_run)

    args = argparse.Namespace(password=None)
    assert cli._resolve_password(args, _parser()) == "from-keychain"


def test_resolve_password_errors_when_no_sources(monkeypatch) -> None:
    monkeypatch.delenv("PCTX_PASSWORD", raising=False)
    monkeypatch.setenv("PCTX_DISABLE_KEYCHAIN", "1")
    args = argparse.Namespace(password=None)
    with pytest.raises(SystemExit):
        cli._resolve_password(args, _parser())
