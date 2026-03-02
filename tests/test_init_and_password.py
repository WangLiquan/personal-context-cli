import os
import subprocess
import sys
from pathlib import Path


def _pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = os.path.abspath("src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not current else f"{src_path}{os.pathsep}{current}"
    return env


def test_init_creates_encrypted_store(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "init",
            "--data-file",
            str(tmp_path / "profile.enc"),
            "--password",
            "pass123",
        ],
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "profile.enc").exists()
