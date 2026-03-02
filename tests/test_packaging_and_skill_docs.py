from __future__ import annotations

import tomllib
from pathlib import Path


def test_pyproject_exposes_console_script_and_runtime_deps() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    scripts = project.get("scripts", {})
    assert scripts.get("personal-context") == "personal_context_cli.cli:main"

    dependencies = project.get("dependencies", [])
    assert any(dep.startswith("cryptography") for dep in dependencies)
    assert any(dep.startswith("pydantic") for dep in dependencies)


def test_skill_docs_use_direct_cli_without_wrapper_script() -> None:
    skill_docs = [
        Path("skills/personal-context-cli-workflow/SKILL.md"),
        Path("skills/personal-context-init-profile/SKILL.md"),
        Path("skills/personal-context-ask-flow/SKILL.md"),
    ]

    for doc in skill_docs:
        content = doc.read_text(encoding="utf-8")
        assert "personal-context " in content
        assert "pctx.sh" not in content


def test_ask_flow_skill_no_api_provider_mentions() -> None:
    files = [
        Path("skills/personal-context-ask-flow/SKILL.md"),
        Path("skills/personal-context-ask-flow/references/command-recipes.md"),
        Path("skills/personal-context-ask-flow/agents/openai.yaml"),
    ]
    for file in files:
        content = file.read_text(encoding="utf-8").lower()
        assert "provider api" not in content
        assert "--provider api" not in content
