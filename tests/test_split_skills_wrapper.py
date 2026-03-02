from __future__ import annotations

import subprocess
from pathlib import Path


def _run_help(script_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_path), "--help"],
        capture_output=True,
        text=True,
    )


def test_init_profile_skill_wrapper_help_runs() -> None:
    script_path = Path("skills/personal-context-init-profile/scripts/pctx.sh")
    result = _run_help(script_path)
    assert result.returncode == 0, result.stderr
    assert "personal-context" in result.stdout


def test_ask_flow_skill_wrapper_help_runs() -> None:
    script_path = Path("skills/personal-context-ask-flow/scripts/pctx.sh")
    result = _run_help(script_path)
    assert result.returncode == 0, result.stderr
    assert "personal-context" in result.stdout
