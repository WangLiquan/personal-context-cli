from __future__ import annotations


def _compact(mapping: dict) -> dict:
    return {key: value for key, value in mapping.items() if value is not None}


def detect_question_type(question: str, question_type: str | None = None) -> str:
    if question_type:
        return question_type

    text = question.lower()
    finance_keywords = ("finance", "fund", "income", "budget", "investment", "cash", "savings")
    career_keywords = ("career", "job", "work", "promotion", "resume", "interview", "salary")
    education_keywords = ("education", "school", "study", "learning", "college", "exam")
    family_keywords = ("family", "spouse", "marriage", "anniversary", "daughter", "son", "parent")

    if any(keyword in text for keyword in finance_keywords):
        return "finance"
    if any(keyword in text for keyword in career_keywords):
        return "career"
    if any(keyword in text for keyword in education_keywords):
        return "education"
    if any(keyword in text for keyword in family_keywords):
        return "family"
    return "other"


def _select_relevant_notes(payload: dict, resolved_type: str) -> list[dict]:
    notes = payload.get("context_notes", [])
    if not isinstance(notes, list):
        return []

    filtered = []
    for item in notes:
        if not isinstance(item, dict):
            continue
        item_type = item.get("question_type")
        if item_type in (None, "", "other", resolved_type):
            filtered.append(item)
    return filtered[-3:]


def _select_relevant_fact_memory(owner: dict, resolved_type: str) -> list[dict]:
    items = owner.get("fact_memory", [])
    if not isinstance(items, list):
        return []

    filtered = []
    for item in items:
        if not isinstance(item, dict):
            continue
        item_type = item.get("question_type")
        if item_type in (None, "", "other", resolved_type):
            filtered.append(item)
    return filtered[-5:]


def find_context_gaps(question: str, question_type: str | None, payload: dict) -> list[str]:
    resolved_type = detect_question_type(question, question_type)
    owner = payload.get("owner_profile", {})
    family_members = payload.get("family_members", [])
    notes = _select_relevant_notes(payload, resolved_type)
    fact_memory = _select_relevant_fact_memory(owner, resolved_type)

    if notes or fact_memory:
        return []

    if resolved_type == "finance":
        has_finance_context = any(owner.get(key) for key in ("income_range", "risk_preference", "goals"))
        return [] if has_finance_context else ["finance_background"]

    if resolved_type == "career":
        has_career_context = any(owner.get(key) for key in ("industry", "age"))
        return [] if has_career_context else ["career_background"]

    if resolved_type == "education":
        has_education_context = any(item.get("occupation_or_school") for item in family_members if isinstance(item, dict))
        return [] if has_education_context else ["education_background"]

    if resolved_type == "family":
        return [] if family_members else ["family_background"]

    has_generic_context = bool(owner or family_members or payload.get("preferences"))
    return [] if has_generic_context else ["general_background"]


def select_context(question: str, question_type: str | None, payload: dict) -> dict:
    resolved_type = detect_question_type(question, question_type)
    owner = payload.get("owner_profile", {})
    notes = _select_relevant_notes(payload, resolved_type)
    fact_memory = _select_relevant_fact_memory(owner, resolved_type)

    if resolved_type == "finance":
        return {
            "owner_profile": _compact(
                {
                    "income_range": owner.get("income_range"),
                    "risk_preference": owner.get("risk_preference"),
                    "goals": owner.get("goals"),
                    "fact_memory": fact_memory,
                }
            ),
            "preferences": payload.get("preferences", {}),
            "family_members": payload.get("family_members", []),
            "context_notes": notes,
        }

    return {
        "owner_profile": {
            **owner,
            "fact_memory": fact_memory,
        },
        "preferences": payload.get("preferences", {}),
        "family_members": payload.get("family_members", []),
        "context_notes": notes,
    }
