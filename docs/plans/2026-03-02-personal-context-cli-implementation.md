# Personal Context CLI Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python CLI that stores personal/family data in local encrypted storage and produces targeted Q&A responses using selective context and optional model API calls.

**Architecture:** A modular local-first app with a CLI layer, encrypted storage layer, domain validation, context selector, and LLM adapter. Real data remains local and encrypted (`*.enc`), while repository content stays open-source safe with templates and docs.

**Tech Stack:** Python 3.11+, `argparse`, `pydantic`, `cryptography`, `httpx`, `pytest`

---

### Task 1: Project Skeleton and CLI Bootstrap

**Files:**
- Create: `pyproject.toml`
- Create: `src/personal_context_cli/__init__.py`
- Create: `src/personal_context_cli/__main__.py`
- Create: `src/personal_context_cli/cli.py`
- Create: `tests/test_cli_smoke.py`

**Step 1: Write the failing test**

```python
# tests/test_cli_smoke.py
import subprocess
import sys


def test_cli_help_contains_core_commands():
    result = subprocess.run(
        [sys.executable, "-m", "personal_context_cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "init" in result.stdout
    assert "ask" in result.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_cli_smoke.py::test_cli_help_contains_core_commands -v`  
Expected: FAIL with `No module named personal_context_cli`.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/cli.py
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="personal-context")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("init")
    sub.add_parser("ask")
    return parser


def main() -> int:
    parser = build_parser()
    parser.parse_args()
    return 0
```

```python
# src/personal_context_cli/__main__.py
from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_cli_smoke.py::test_cli_help_contains_core_commands -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add pyproject.toml src/personal_context_cli/__init__.py src/personal_context_cli/__main__.py src/personal_context_cli/cli.py tests/test_cli_smoke.py
git commit -m "feat: bootstrap python cli project"
```

### Task 2: Encryption Primitives (`secure_store` foundation)

**Files:**
- Create: `src/personal_context_cli/crypto.py`
- Create: `tests/test_crypto.py`

**Step 1: Write the failing test**

```python
# tests/test_crypto.py
from personal_context_cli.crypto import decrypt_payload, encrypt_payload


def test_encrypt_decrypt_roundtrip():
    payload = {"owner_profile": {"industry": "tech"}}
    token = encrypt_payload(payload, "pass123")
    restored = decrypt_payload(token, "pass123")
    assert restored == payload
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_crypto.py::test_encrypt_decrypt_roundtrip -v`  
Expected: FAIL with import error for `personal_context_cli.crypto`.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/crypto.py
import base64
import json
from hashlib import scrypt
from cryptography.fernet import Fernet


def _derive_key(password: str, salt: bytes) -> bytes:
    key = scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return base64.urlsafe_b64encode(key)


def encrypt_payload(data: dict, password: str) -> bytes:
    salt = b"local-fixed-salt-v1"
    f = Fernet(_derive_key(password, salt))
    raw = json.dumps(data, ensure_ascii=True).encode("utf-8")
    return f.encrypt(raw)


def decrypt_payload(token: bytes, password: str) -> dict:
    salt = b"local-fixed-salt-v1"
    f = Fernet(_derive_key(password, salt))
    return json.loads(f.decrypt(token).decode("utf-8"))
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_crypto.py::test_encrypt_decrypt_roundtrip -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/crypto.py tests/test_crypto.py
git commit -m "feat: add password-based encryption primitives"
```

### Task 3: Encrypted File Store Read/Write

**Files:**
- Create: `src/personal_context_cli/store.py`
- Create: `tests/test_store.py`

**Step 1: Write the failing test**

```python
# tests/test_store.py
from pathlib import Path
from personal_context_cli.store import EncryptedStore


def test_store_writes_encrypted_file_only(tmp_path: Path):
    store = EncryptedStore(tmp_path / "profile.enc")
    store.save({"owner_profile": {"age": 30}}, "pass123")
    assert (tmp_path / "profile.enc").exists()
    assert not (tmp_path / "profile.json").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_store.py::test_store_writes_encrypted_file_only -v`  
Expected: FAIL with import error for `EncryptedStore`.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/store.py
from pathlib import Path
from .crypto import decrypt_payload, encrypt_payload


class EncryptedStore:
    def __init__(self, path: Path):
        self.path = path

    def save(self, data: dict, password: str) -> None:
        self.path.write_bytes(encrypt_payload(data, password))

    def load(self, password: str) -> dict:
        return decrypt_payload(self.path.read_bytes(), password)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_store.py::test_store_writes_encrypted_file_only -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/store.py tests/test_store.py
git commit -m "feat: add encrypted local store"
```

### Task 4: Domain Schema and Validation

**Files:**
- Create: `src/personal_context_cli/models.py`
- Create: `tests/test_models.py`

**Step 1: Write the failing test**

```python
# tests/test_models.py
import pytest
from pydantic import ValidationError
from personal_context_cli.models import OwnerProfile


def test_owner_profile_requires_valid_age():
    with pytest.raises(ValidationError):
        OwnerProfile(age=-1, industry="tech", income_range="30-50w")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py::test_owner_profile_requires_valid_age -v`  
Expected: FAIL with import error for `OwnerProfile`.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/models.py
from pydantic import BaseModel, Field


class OwnerProfile(BaseModel):
    age: int = Field(ge=0, le=120)
    industry: str
    income_range: str
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_models.py::test_owner_profile_requires_valid_age -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/models.py tests/test_models.py
git commit -m "feat: add domain models with validation"
```

### Task 5: `init` + Password Rotation Commands

**Files:**
- Modify: `src/personal_context_cli/cli.py`
- Create: `src/personal_context_cli/config.py`
- Create: `tests/test_init_and_password.py`

**Step 1: Write the failing test**

```python
# tests/test_init_and_password.py
import subprocess
import sys
from pathlib import Path


def test_init_creates_encrypted_store(tmp_path: Path):
    result = subprocess.run(
        [
            sys.executable, "-m", "personal_context_cli", "init",
            "--data-file", str(tmp_path / "profile.enc"),
            "--password", "pass123"
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (tmp_path / "profile.enc").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_init_and_password.py::test_init_creates_encrypted_store -v`  
Expected: FAIL because `init` command is not implemented.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/cli.py (core shape)
# add init parser options and handler:
# - --data-file (required path)
# - --password (required for v1 CLI automation)
# handler creates default payload and writes encrypted store
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_init_and_password.py::test_init_creates_encrypted_store -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/cli.py src/personal_context_cli/config.py tests/test_init_and_password.py
git commit -m "feat: implement init command with encrypted bootstrap"
```

### Task 6: Profile/Prefs and Family CRUD Commands

**Files:**
- Modify: `src/personal_context_cli/cli.py`
- Modify: `src/personal_context_cli/models.py`
- Create: `src/personal_context_cli/services.py`
- Create: `tests/test_profile_family_commands.py`

**Step 1: Write the failing test**

```python
# tests/test_profile_family_commands.py
import subprocess
import sys


def test_profile_set_and_get_roundtrip(tmp_path):
    data_file = tmp_path / "profile.enc"
    subprocess.run(
        [sys.executable, "-m", "personal_context_cli", "init", "--data-file", str(data_file), "--password", "pass123"],
        check=True,
    )
    set_result = subprocess.run(
        [
            sys.executable, "-m", "personal_context_cli", "profile", "set",
            "--data-file", str(data_file), "--password", "pass123",
            "--age", "32", "--industry", "internet", "--income-range", "50-100w"
        ],
        capture_output=True, text=True
    )
    get_result = subprocess.run(
        [sys.executable, "-m", "personal_context_cli", "profile", "get", "--data-file", str(data_file), "--password", "pass123"],
        capture_output=True, text=True
    )
    assert set_result.returncode == 0
    assert get_result.returncode == 0
    assert "internet" in get_result.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_profile_family_commands.py::test_profile_set_and_get_roundtrip -v`  
Expected: FAIL because subcommands are not implemented.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/services.py
# add service functions to:
# - load payload
# - update owner_profile / preferences
# - add/list/update/remove family members
# - persist payload through EncryptedStore
```

```python
# src/personal_context_cli/cli.py
# add command tree:
# profile set/get
# prefs set/get
# family add/list/update/remove
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_profile_family_commands.py::test_profile_set_and_get_roundtrip -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/cli.py src/personal_context_cli/models.py src/personal_context_cli/services.py tests/test_profile_family_commands.py
git commit -m "feat: add profile prefs and family management commands"
```

### Task 7: Context Selector and `context preview`

**Files:**
- Create: `src/personal_context_cli/context_selector.py`
- Modify: `src/personal_context_cli/cli.py`
- Create: `tests/test_context_selector.py`
- Create: `tests/test_context_preview_command.py`

**Step 1: Write the failing test**

```python
# tests/test_context_selector.py
from personal_context_cli.context_selector import select_context


def test_finance_question_selects_finance_fields_only():
    payload = {
        "owner_profile": {"industry": "tech", "income_range": "50-100w", "age": 32},
        "preferences": {"response_style": "brief"},
        "family_members": [{"relation": "spouse", "focus_areas": ["education"]}],
    }
    ctx = select_context("Should I increase my emergency fund?", "finance", payload)
    assert "income_range" in ctx["owner_profile"]
    assert "industry" not in ctx["owner_profile"]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_context_selector.py::test_finance_question_selects_finance_fields_only -v`  
Expected: FAIL because selector module is missing.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/context_selector.py
def select_context(question: str, question_type: str, payload: dict) -> dict:
    if question_type == "finance":
        owner = payload.get("owner_profile", {})
        return {
            "owner_profile": {
                "income_range": owner.get("income_range"),
                "risk_preference": owner.get("risk_preference"),
                "goals": owner.get("goals"),
            },
            "preferences": payload.get("preferences", {}),
            "family_members": payload.get("family_members", []),
        }
    return {"owner_profile": payload.get("owner_profile", {}), "preferences": payload.get("preferences", {})}
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_context_selector.py::test_finance_question_selects_finance_fields_only -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/context_selector.py src/personal_context_cli/cli.py tests/test_context_selector.py tests/test_context_preview_command.py
git commit -m "feat: add selective context extraction and preview command"
```

### Task 8: LLM Adapter and `ask` Command (with fallback)

**Files:**
- Create: `src/personal_context_cli/llm_adapter.py`
- Modify: `src/personal_context_cli/cli.py`
- Create: `tests/test_ask_command.py`

**Step 1: Write the failing test**

```python
# tests/test_ask_command.py
import os
from personal_context_cli.llm_adapter import generate_answer


def test_generate_answer_falls_back_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = generate_answer("How to plan next year?", {"owner_profile": {"income_range": "50-100w"}})
    assert "API key not configured" in text
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_ask_command.py::test_generate_answer_falls_back_without_api_key -v`  
Expected: FAIL because `llm_adapter` does not exist.

**Step 3: Write minimal implementation**

```python
# src/personal_context_cli/llm_adapter.py
import os


def generate_answer(question: str, context: dict) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        return f"API key not configured. Use this context externally: {context}"
    return "stub-answer"
```

```python
# src/personal_context_cli/cli.py
# add ask command:
# - load encrypted payload
# - select context via context_selector
# - call generate_answer
# - print answer
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_ask_command.py::test_generate_answer_falls_back_without_api_key -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/personal_context_cli/llm_adapter.py src/personal_context_cli/cli.py tests/test_ask_command.py
git commit -m "feat: add ask command and llm fallback behavior"
```

### Task 9: Open-Source Safety, Docs, and End-to-End Verification

**Files:**
- Create: `.gitignore`
- Create: `.env.example`
- Create: `profile.example.json`
- Create: `README.md`
- Create: `LICENSE`
- Create: `SECURITY.md`
- Create: `CONTRIBUTING.md`
- Create: `tests/test_gitignore_safety.py`

**Step 1: Write the failing test**

```python
# tests/test_gitignore_safety.py
from pathlib import Path


def test_gitignore_blocks_sensitive_files():
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert "*.enc" in text
    assert ".env" in text
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_gitignore_safety.py::test_gitignore_blocks_sensitive_files -v`  
Expected: FAIL because `.gitignore` does not exist yet.

**Step 3: Write minimal implementation**

```gitignore
# .gitignore
__pycache__/
.pytest_cache/
.venv/
*.enc
.env
```

```markdown
# README.md
- quickstart
- command reference
- local encryption model
- safe open-source workflow
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_gitignore_safety.py::test_gitignore_blocks_sensitive_files -v`  
Expected: PASS.

Then run full suite: `pytest -v`  
Expected: all tests PASS.

**Step 5: Commit**

```bash
git add .gitignore .env.example profile.example.json README.md LICENSE SECURITY.md CONTRIBUTING.md tests/test_gitignore_safety.py
git commit -m "docs: add open-source safety and project documentation"
```

### Task 10: Final Quality Gate (@verification-before-completion)

**Files:**
- Modify: `docs/plans/2026-03-02-personal-context-cli-design.md` (optional traceability notes)
- Create: `docs/plans/2026-03-02-personal-context-cli-acceptance.md`

**Step 1: Write the failing acceptance check list**

```markdown
# Acceptance Checklist
- init creates encrypted file
- profile/family/prefs CRUD works
- context preview is selective
- ask works with fallback when API key missing
- no plaintext sensitive file tracked by git
```

**Step 2: Run verification commands to prove current status**

Run: `pytest -v`  
Expected: PASS.

Run: `git status --short`  
Expected: clean working tree.

**Step 3: Write minimal implementation**

```markdown
# docs/plans/2026-03-02-personal-context-cli-acceptance.md
- fill each checklist item with evidence (test name + command output summary)
```

**Step 4: Re-run verification**

Run: `pytest -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add docs/plans/2026-03-02-personal-context-cli-acceptance.md docs/plans/2026-03-02-personal-context-cli-design.md
git commit -m "chore: add acceptance evidence and final verification"
```

---

## Execution Notes

- Apply strict RED-GREEN-REFACTOR for every task using @test-driven-development.
- If any unexpected behavior appears, switch to @systematic-debugging before changing implementation.
- Before claiming completion, run @verification-before-completion checks and capture evidence.
