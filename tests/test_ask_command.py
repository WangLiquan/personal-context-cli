from __future__ import annotations

import subprocess

import pytest

from personal_context_cli.llm_adapter import generate_answer


def test_generate_answer_api_provider_is_not_supported() -> None:
    with pytest.raises(ValueError, match="Unsupported provider: api"):
        generate_answer(
            "How to plan next year?",
            {"owner_profile": {"income_range": "50-100w"}},
            provider="api",
        )


def test_generate_answer_auto_uses_codex(monkeypatch) -> None:
    def fake_which(name: str) -> str | None:
        return "/usr/bin/codex" if name == "codex" else None

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert args[0][0] == "codex"
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="codex-output", stderr="")

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)
    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert text == "codex-output"


def test_generate_answer_auto_uses_claude_when_codex_missing(monkeypatch) -> None:
    def fake_which(name: str) -> str | None:
        if name == "codex":
            return None
        if name == "claude":
            return "/usr/bin/claude"
        return None

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert args[0][0] == "claude"
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="claude-output", stderr="")

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)
    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)
    monkeypatch.delenv("CLAUDECODE", raising=False)

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert text == "claude-output"


def test_generate_answer_auto_returns_host_auth_guidance_when_no_cli(monkeypatch) -> None:
    def fake_which(name: str) -> str | None:
        return None

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert "No relay provider available" in text
    assert "OpenX or Claude Code" in text
    assert "API key" not in text


def test_generate_answer_codex_retries_on_timeout(monkeypatch) -> None:
    calls = 0

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal calls
        calls += 1
        if calls == 1:
            raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="retry-success", stderr="")

    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)

    text = generate_answer(
        "question",
        {"k": "v"},
        provider="codex",
        relay_timeout_seconds=1,
        relay_retries=1,
    )
    assert text == "retry-success"
    assert calls == 2


def test_generate_answer_auto_reports_provider_failures(monkeypatch) -> None:
    def fake_which(name: str) -> str | None:
        if name in {"codex", "claude"}:
            return f"/usr/bin/{name}"
        return None

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        if args[0][0] == "codex":
            return subprocess.CompletedProcess(
                args=args[0],
                returncode=1,
                stdout="",
                stderr="ssh: Could not resolve hostname github.com",
            )
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=1,
            stdout="",
            stderr="Please run claude auth login",
        )

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)
    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)
    monkeypatch.delenv("CLAUDECODE", raising=False)

    text = generate_answer(
        "question",
        {"k": "v"},
        provider="auto",
        relay_timeout_seconds=1,
        relay_retries=0,
    )
    assert "Relay providers unavailable" in text
    assert "codex: network_unreachable" in text
    assert "claude: auth_required" in text
    assert "API key" not in text


def test_generate_answer_auto_uses_claude_in_claudecode_env(monkeypatch) -> None:
    """CLAUDECODE env must not block claude relay in auto mode."""
    def fake_which(name: str) -> str | None:
        if name == "claude":
            return "/usr/bin/claude"
        return None

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        assert args[0][0] == "claude"
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="claude-output", stderr="")

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)
    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)
    monkeypatch.setenv("CLAUDECODE", "1")

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert text == "claude-output"


def test_generate_answer_auto_parallel_first_success_wins(monkeypatch) -> None:
    """When both providers are available, first successful result wins."""
    def fake_which(name: str) -> str | None:
        if name in {"codex", "claude"}:
            return f"/usr/bin/{name}"
        return None

    def fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        if args[0][0] == "codex":
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="codex-wins", stderr="")
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="claude-wins", stderr="")

    monkeypatch.setattr("personal_context_cli.llm_adapter.shutil.which", fake_which)
    monkeypatch.setattr("personal_context_cli.llm_adapter.subprocess.run", fake_run)
    monkeypatch.delenv("CLAUDECODE", raising=False)

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert text in ("codex-wins", "claude-wins")
