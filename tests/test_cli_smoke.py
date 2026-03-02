import os
import subprocess
import sys
import unittest


def _pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src_path = os.path.abspath("src")
    current = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src_path if not current else f"{src_path}{os.pathsep}{current}"
    return env


class CLISmokeTest(unittest.TestCase):
    def test_cli_help_contains_core_commands(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "personal_context_cli", "--help"],
            capture_output=True,
            text=True,
            env=_pythonpath_env(),
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("init", result.stdout)
        self.assertIn("ask", result.stdout)


if __name__ == "__main__":
    unittest.main()
