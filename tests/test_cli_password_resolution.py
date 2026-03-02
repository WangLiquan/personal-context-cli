from __future__ import annotations

import argparse

import pytest

from personal_context_cli import cli


def _parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(prog="personal-context")


def test_resolve_password_prefers_explicit_flag() -> None:
    args = argparse.Namespace(password="pass123")
    assert cli._resolve_password(args, _parser()) == "pass123"


def test_resolve_password_prompts_in_interactive_mode(monkeypatch) -> None:
    args = argparse.Namespace(password=None)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("personal_context_cli.cli.getpass.getpass", lambda _: "typed-pass")
    assert cli._resolve_password(args, _parser()) == "typed-pass"


def test_resolve_password_errors_in_non_interactive_mode(monkeypatch) -> None:
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: False)
    args = argparse.Namespace(password=None)
    with pytest.raises(SystemExit):
        cli._resolve_password(args, _parser())
