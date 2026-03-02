from pathlib import Path


def test_gitignore_blocks_sensitive_files() -> None:
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert "*.enc" in text
    assert ".env" in text
