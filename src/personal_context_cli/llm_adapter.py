from __future__ import annotations

import json
import os
import shutil
import subprocess


def _build_relay_prompt(question: str, context: dict) -> str:
    return (
        "You are a practical personal decision assistant. "
        "Use the provided context and answer the user's question clearly.\n\n"
        f"Question: {question}\n"
        f"Context: {json.dumps(context, ensure_ascii=False)}"
    )


def _run_relay_command(command: list[str], prompt: str) -> str:
    try:
        result = subprocess.run(
            [*command, prompt],
            capture_output=True,
            text=True,
            timeout=20,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"relay provider timeout: {' '.join(command)}") from exc
    if result.returncode != 0:
        error = (result.stderr or result.stdout).strip()
        raise RuntimeError(error or "relay provider execution failed")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError("relay provider returned empty output")
    return output


def _generate_with_api_fallback(context: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return f"API key not configured. Use this context externally: {context}"
    return "stub-answer"


def generate_answer(question: str, context: dict, provider: str = "auto") -> str:
    prompt = _build_relay_prompt(question, context)

    if provider == "auto":
        if shutil.which("codex"):
            try:
                return _run_relay_command(
                    ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"],
                    prompt,
                )
            except RuntimeError:
                pass
        if shutil.which("claude"):
            try:
                return _run_relay_command(["claude", "-p"], prompt)
            except RuntimeError:
                pass
        return _generate_with_api_fallback(context)

    if provider == "codex":
        return _run_relay_command(
            ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"],
            prompt,
        )

    if provider == "claude":
        return _run_relay_command(["claude", "-p"], prompt)

    if provider == "api":
        return _generate_with_api_fallback(context)

    raise ValueError(f"Unsupported provider: {provider}")
