from __future__ import annotations

import subprocess

from personal_context_cli.llm_adapter import generate_answer


def test_generate_answer_api_fallback_without_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = generate_answer(
        "How to plan next year?",
        {"owner_profile": {"income_range": "50-100w"}},
        provider="api",
    )
    assert "API key not configured" in text


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

    text = generate_answer("question", {"k": "v"}, provider="auto")
    assert text == "claude-output"
