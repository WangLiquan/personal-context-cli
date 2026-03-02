from __future__ import annotations

from pathlib import Path

from personal_context_cli import cli
from personal_context_cli.config import DEFAULT_PROFILE_PAYLOAD
from personal_context_cli.store import EncryptedStore


def _run_ask(
    monkeypatch,
    data_file: Path,
    question: str,
    password: str = "pass123",
) -> tuple[int, str]:
    monkeypatch.setattr(
        "personal_context_cli.cli.sys.argv",
        [
            "personal-context",
            "ask",
            question,
            "--provider",
            "auto",
            "--data-file",
            str(data_file),
            "--password",
            password,
        ],
    )
    code = cli.main()
    return code


def test_ask_prompts_and_persists_context_note_when_context_missing(monkeypatch, tmp_path, capsys) -> None:
    data_file = tmp_path / "profile.enc"
    EncryptedStore(data_file).save(DEFAULT_PROFILE_PAYLOAD, "pass123")

    captured: dict[str, object] = {}

    def fake_generate_answer(question: str, context: dict, **_: object) -> str:
        captured["question"] = question
        captured["context"] = context
        return "mock-answer"

    monkeypatch.setattr("personal_context_cli.cli.generate_answer", fake_generate_answer)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: "我的月收入 5w，风险偏好中等。")

    code = _run_ask(monkeypatch, data_file, "Should I increase my emergency fund?")

    assert code == 0
    assert capsys.readouterr().out.strip() == "mock-answer"

    payload = EncryptedStore(data_file).load("pass123")
    history = payload.get("ask_history", [])
    assert len(history) == 1
    assert history[0]["question"] == "Should I increase my emergency fund?"
    assert history[0]["question_type"] == "finance"

    notes = payload.get("context_notes", [])
    assert len(notes) == 1
    assert notes[0]["note"] == "我的月收入 5w，风险偏好中等。"
    assert notes[0]["question_type"] == "finance"

    fact_memory = payload.get("owner_profile", {}).get("fact_memory", [])
    assert any(item.get("fact") == "月收入约5w" for item in fact_memory)
    assert any(item.get("fact") == "风险偏好中等" for item in fact_memory)

    context = captured["context"]
    assert isinstance(context, dict)
    assert len(context["context_notes"]) == 1
    assert context["context_notes"][0]["note"] == "我的月收入 5w，风险偏好中等。"
    assert any(item.get("fact") == "月收入约5w" for item in context["owner_profile"]["fact_memory"])


def test_ask_skips_follow_up_when_context_is_already_sufficient_but_persists_question(
    monkeypatch, tmp_path, capsys
) -> None:
    data_file = tmp_path / "profile.enc"
    payload = dict(DEFAULT_PROFILE_PAYLOAD)
    payload["owner_profile"] = {"income_range": "50-100w"}
    EncryptedStore(data_file).save(payload, "pass123")

    def fake_generate_answer(question: str, context: dict, **_: object) -> str:
        return "mock-answer"

    monkeypatch.setattr("personal_context_cli.cli.generate_answer", fake_generate_answer)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: True)

    def fail_input(_: str) -> str:
        raise AssertionError("input() should not be called when context is already sufficient")

    monkeypatch.setattr("builtins.input", fail_input)

    code = _run_ask(monkeypatch, data_file, "Should I increase my emergency fund?")

    assert code == 0
    assert capsys.readouterr().out.strip() == "mock-answer"

    saved = EncryptedStore(data_file).load("pass123")
    notes = saved.get("context_notes", [])
    assert notes == []

    history = saved.get("ask_history", [])
    assert len(history) == 1
    assert history[0]["question"] == "Should I increase my emergency fund?"
    assert history[0]["question_type"] == "finance"


def test_ask_extracts_mortgage_fact_into_profile_memory(monkeypatch, tmp_path, capsys) -> None:
    data_file = tmp_path / "profile.enc"
    EncryptedStore(data_file).save(DEFAULT_PROFILE_PAYLOAD, "pass123")

    def fake_generate_answer(question: str, context: dict, **_: object) -> str:
        return "mock-answer"

    monkeypatch.setattr("personal_context_cli.cli.generate_answer", fake_generate_answer)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: False)

    code = _run_ask(monkeypatch, data_file, "我每月房贷6000块，怎么优化现金流？")
    assert code == 0
    assert capsys.readouterr().out.strip() == "mock-answer"

    payload = EncryptedStore(data_file).load("pass123")
    fact_memory = payload.get("owner_profile", {}).get("fact_memory", [])
    assert any(item.get("fact") == "房贷每月约6000块" for item in fact_memory)
