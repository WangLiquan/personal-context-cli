from personal_context_cli.context_selector import select_context


def test_finance_question_selects_finance_fields_only() -> None:
    payload = {
        "owner_profile": {"industry": "tech", "income_range": "50-100w", "age": 32},
        "preferences": {"response_style": "brief"},
        "family_members": [{"relation": "spouse", "focus_areas": ["education"]}],
    }
    context = select_context(
        "Should I increase my emergency fund?",
        "finance",
        payload,
    )
    assert "income_range" in context["owner_profile"]
    assert "industry" not in context["owner_profile"]
