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
        Path("skills/personal-context-reinit/SKILL.md"),
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


def test_ask_flow_docs_do_not_require_type_flag() -> None:
    files = [
        Path("skills/personal-context-ask-flow/SKILL.md"),
        Path("skills/personal-context-ask-flow/references/command-recipes.md"),
    ]
    for file in files:
        content = file.read_text(encoding="utf-8")
        assert "--type" not in content


def test_skill_docs_use_explicit_password_examples() -> None:
    skill_docs = [
        Path("skills/personal-context-cli-workflow/SKILL.md"),
        Path("skills/personal-context-init-profile/SKILL.md"),
        Path("skills/personal-context-ask-flow/SKILL.md"),
        Path("skills/personal-context-reinit/SKILL.md"),
    ]
    for doc in skill_docs:
        content = doc.read_text(encoding="utf-8")
        assert "--password" in content
        assert "PCTX_PASSWORD" not in content


def test_readme_documents_explicit_password_usage() -> None:
    content = Path("README.md").read_text(encoding="utf-8")
    assert "--password" in content
    assert "PCTX_PASSWORD" not in content


def test_chinese_readme_documents_explicit_password_usage() -> None:
    content = Path("README.zh-CN.md").read_text(encoding="utf-8")
    assert "--password" in content
    assert "PCTX_PASSWORD" not in content
    assert "personal-context-reinit" in content


def test_init_skill_requests_password_first() -> None:
    content = Path("skills/personal-context-init-profile/SKILL.md").read_text(encoding="utf-8")
    assert "Ask the user for a password before running any init/profile command." in content


def test_init_skill_disallows_default_password_option() -> None:
    skill_content = Path("skills/personal-context-init-profile/SKILL.md").read_text(encoding="utf-8")
    prompt_content = Path("skills/personal-context-init-profile/agents/openai.yaml").read_text(encoding="utf-8")
    assert "Do not offer a default password option." in skill_content
    assert "Never offer a default password option" in prompt_content


def test_reinit_skill_defines_full_reset_workflow() -> None:
    content = Path("skills/personal-context-reinit/SKILL.md").read_text(encoding="utf-8")
    assert "clear all existing personal-context settings" in content.lower()
    assert "personal-context init" in content
    assert "reconfigure profile, preferences, and family data" in content.lower()
