from __future__ import annotations

import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    env = os.environ.copy()
    env.pop("CLAUDECODE", None)

    for attempt in range(attempts):
        try:
            result = subprocess.run(
                [*command, prompt],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=env,
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


def _generate_host_auth_guidance(context: dict) -> str:
    return (
        "No relay provider available. Run this command inside OpenX or Claude Code "
        f"with an active login session. Use this context externally: {context}"
    )


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
        available: list[tuple[str, list[str]]] = []
        if shutil.which("codex"):
            available.append(("codex", ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only"]))
        if shutil.which("claude"):
            available.append(("claude", ["claude", "-p"]))

        if not available:
            return _generate_host_auth_guidance(context)

        with ThreadPoolExecutor(max_workers=len(available)) as executor:
            futures = {
                executor.submit(
                    _run_relay_command,
                    cmd,
                    prompt,
                    timeout_seconds=timeout_seconds,
                    retries=retries,
                ): name
                for name, cmd in available
            }
            relay_failures: list[str] = []
            for future in as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    # Cancel remaining futures on first success
                    for f in futures:
                        f.cancel()
                    return result
                except RuntimeError as exc:
                    relay_failures.append(f"{name}: {_classify_provider_error(str(exc))}")

        fallback = _generate_host_auth_guidance(context)
        details = "; ".join(relay_failures)
        return f"Relay providers unavailable ({details}). {fallback}"

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

    raise ValueError(f"Unsupported provider: {provider}")
