from __future__ import annotations

from pathlib import Path

from personal_context_cli import cli
from personal_context_cli.config import DEFAULT_PROFILE_PAYLOAD
from personal_context_cli.store import EncryptedStore


def _run_ask(
    monkeypatch,
    data_file: Path,
    question: str,
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

    monkeypatch.setenv("PCTX_PASSWORD", "pass123")
    monkeypatch.setattr("personal_context_cli.cli._read_password_from_keychain", lambda: None)
    monkeypatch.setattr("personal_context_cli.cli.generate_answer", fake_generate_answer)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _: "我的月收入 5w，风险偏好中等。")

    code = _run_ask(monkeypatch, data_file, "Should I increase my emergency fund?")

    assert code == 0
    assert capsys.readouterr().out.strip() == "mock-answer"

    payload = EncryptedStore(data_file).load("pass123")
    notes = payload.get("context_notes", [])
    assert len(notes) == 1
    assert notes[0]["note"] == "我的月收入 5w，风险偏好中等。"
    assert notes[0]["question_type"] == "finance"

    context = captured["context"]
    assert isinstance(context, dict)
    assert context["context_notes"][0]["note"] == "我的月收入 5w，风险偏好中等。"


def test_ask_skips_follow_up_when_context_is_already_sufficient(monkeypatch, tmp_path, capsys) -> None:
    data_file = tmp_path / "profile.enc"
    payload = dict(DEFAULT_PROFILE_PAYLOAD)
    payload["owner_profile"] = {"income_range": "50-100w"}
    EncryptedStore(data_file).save(payload, "pass123")

    def fake_generate_answer(question: str, context: dict, **_: object) -> str:
        return "mock-answer"

    monkeypatch.setenv("PCTX_PASSWORD", "pass123")
    monkeypatch.setattr("personal_context_cli.cli._read_password_from_keychain", lambda: None)
    monkeypatch.setattr("personal_context_cli.cli.generate_answer", fake_generate_answer)
    monkeypatch.setattr("personal_context_cli.cli.sys.stdin.isatty", lambda: True)

    def fail_input(_: str) -> str:
        raise AssertionError("input() should not be called when context is already sufficient")

    monkeypatch.setattr("builtins.input", fail_input)

    code = _run_ask(monkeypatch, data_file, "Should I increase my emergency fund?")

    assert code == 0
    assert capsys.readouterr().out.strip() == "mock-answer"

    saved = EncryptedStore(data_file).load("pass123")
    assert saved.get("context_notes", []) == []
