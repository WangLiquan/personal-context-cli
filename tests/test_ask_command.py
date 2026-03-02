from personal_context_cli.llm_adapter import generate_answer


def test_generate_answer_falls_back_without_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = generate_answer(
        "How to plan next year?",
        {"owner_profile": {"income_range": "50-100w"}},
    )
    assert "API key not configured" in text
