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


def _run_relay_command(
    command: list[str],
    prompt: str,
    *,
    timeout_seconds: int,
    retries: int,
) -> str:
    attempts = max(1, retries + 1)

    for attempt in range(attempts):
        try:
            result = subprocess.run(
                [*command, prompt],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            if attempt == attempts - 1:
                raise RuntimeError(f"relay provider timeout: {' '.join(command)}") from exc
            continue

        if result.returncode != 0:
            error = (result.stderr or result.stdout).strip()
            raise RuntimeError(error or "relay provider execution failed")

        output = result.stdout.strip()
        if not output:
            raise RuntimeError("relay provider returned empty output")
        return output

    raise RuntimeError("relay provider execution failed")


def _generate_with_api_fallback(context: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return f"API key not configured. Use this context externally: {context}"
    return "stub-answer"


def _classify_provider_error(error_message: str) -> str:
    text = error_message.lower()
    network_signatures = [
        "could not resolve host",
        "could not resolve hostname",
        "name or service not known",
        "network is unreachable",
        "temporary failure in name resolution",
        "connection timed out",
        "failed to connect",
        "dns",
    ]
    auth_signatures = [
        "auth",
        "unauthorized",
        "forbidden",
        "api key",
        "token",
        "login",
        "permission denied",
    ]

    if any(sig in text for sig in network_signatures):
        return "network_unreachable"
    if any(sig in text for sig in auth_signatures):
        return "auth_required"
    if "timeout" in text:
        return "timeout"
    return "execution_failed"


def generate_answer(
    question: str,
    context: dict,
    provider: str = "auto",
    *,
    relay_timeout_seconds: int = 20,
    relay_retries: int = 0,
) -> str:
    prompt = _build_relay_prompt(question, context)
    timeout_seconds = max(1, relay_timeout_seconds)
    retries = max(0, relay_retries)

    if provider == "auto":
        relay_failures: list[str] = []

        if shutil.which("codex"):
            try:
                return _run_relay_command(
                    ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"],
                    prompt,
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                )
            except RuntimeError as exc:
                relay_failures.append(f"codex: {_classify_provider_error(str(exc))}")
        if shutil.which("claude"):
            try:
                return _run_relay_command(
                    ["claude", "-p"],
                    prompt,
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                )
            except RuntimeError as exc:
                relay_failures.append(f"claude: {_classify_provider_error(str(exc))}")

        fallback = _generate_with_api_fallback(context)
        if relay_failures:
            details = "; ".join(relay_failures)
            return f"Relay providers unavailable ({details}). {fallback}"
        return fallback

    if provider == "codex":
        return _run_relay_command(
            ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"],
            prompt,
            timeout_seconds=timeout_seconds,
            retries=retries,
        )

    if provider == "claude":
        return _run_relay_command(
            ["claude", "-p"],
            prompt,
            timeout_seconds=timeout_seconds,
            retries=retries,
        )

    if provider == "api":
        return _generate_with_api_fallback(context)

    raise ValueError(f"Unsupported provider: {provider}")
