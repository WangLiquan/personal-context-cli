import os
import subprocess
import sys


def _pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = os.path.abspath("src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not current else f"{src_path}{os.pathsep}{current}"
    return env


def test_profile_set_and_get_roundtrip(tmp_path) -> None:
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
    assert set_result.returncode == 0, set_result.stderr
    assert get_result.returncode == 0, get_result.stderr
    assert "internet" in get_result.stdout
