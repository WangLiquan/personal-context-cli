from __future__ import annotations


def _compact(mapping: dict) -> dict:
    return {key: value for key, value in mapping.items() if value is not None}


def _detect_question_type(question: str) -> str:
    text = question.lower()
    finance_keywords = ("finance", "fund", "income", "budget", "investment", "cash")
    if any(keyword in text for keyword in finance_keywords):
        return "finance"
    return "other"


def select_context(question: str, question_type: str | None, payload: dict) -> dict:
    resolved_type = question_type or _detect_question_type(question)
    owner = payload.get("owner_profile", {})

    if resolved_type == "finance":
        return {
            "owner_profile": _compact(
                {
                    "income_range": owner.get("income_range"),
                    "risk_preference": owner.get("risk_preference"),
                    "goals": owner.get("goals"),
                }
            ),
            "preferences": payload.get("preferences", {}),
            "family_members": payload.get("family_members", []),
        }

    return {
        "owner_profile": owner,
        "preferences": payload.get("preferences", {}),
        "family_members": payload.get("family_members", []),
    }
