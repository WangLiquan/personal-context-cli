import subprocess
from pathlib import Path


def test_skill_wrapper_help_runs() -> None:
    script_path = Path("skills/personal-context-cli-workflow/scripts/pctx.sh")
    result = subprocess.run(
        ["bash", str(script_path), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "personal-context" in result.stdout
