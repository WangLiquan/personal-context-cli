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


def test_profile_get_with_explicit_password_roundtrip(tmp_path: Path) -> None:
    data_file = tmp_path / "profile.enc"
    init_result = subprocess.run(
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
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert init_result.returncode == 0, init_result.stderr

    set_result = subprocess.run(
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
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert set_result.returncode == 0, set_result.stderr

    get_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "profile",
            "get",
            "--data-file",
            str(data_file),
            "--password",
            "pass123",
        ],
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert get_result.returncode == 0, get_result.stderr
    assert "internet" in get_result.stdout


def test_profile_get_requires_password_in_non_interactive_mode(tmp_path: Path) -> None:
    data_file = tmp_path / "profile.enc"
    init_result = subprocess.run(
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
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert init_result.returncode == 0, init_result.stderr

    get_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "personal_context_cli",
            "profile",
            "get",
            "--data-file",
            str(data_file),
        ],
        capture_output=True,
        text=True,
        env=_pythonpath_env(),
    )
    assert get_result.returncode != 0
    assert "Password not provided. Use --password or run in interactive mode." in get_result.stderr
