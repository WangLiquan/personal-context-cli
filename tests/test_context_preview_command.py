import os
import subprocess
import sys


def _pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = os.path.abspath("src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not current else f"{src_path}{os.pathsep}{current}"
    return env


def test_context_preview_selective_output(tmp_path) -> None:
    data_file = tmp_path / "profile.enc"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "init",
            "--data-file",
            str(data_file),
            "--password",
            "pass123",
        ],
        check=True,
        env=_pythonpath_env(),
    )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "profile",
            "set",
            "--data-file",
            str(data_file),
            "--password",
            "pass123",
            "--age",
            "32",
            "--industry",
            "internet",
            "--income-range",
            "50-100w",
        ],
        check=True,
        env=_pythonpath_env(),
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "context",
            "preview",
            "Should I increase my emergency fund?",
            "--type",
            "finance",
            "--data-file",
            str(data_file),
            "--password",
            "pass123",
        ],
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )

    assert result.returncode == 0, result.stderr
    assert "income_range" in result.stdout
    assert "industry" not in result.stdout
