from __future__ import annotations

import os


def generate_answer(question: str, context: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return f"API key not configured. Use this context externally: {context}"
    return "stub-answer"
