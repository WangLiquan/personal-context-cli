# Personal Context CLI Acceptance

Date: 2026-03-02

## Checklist With Evidence

### 1) init creates encrypted file

- Evidence test: `tests/test_init_and_password.py::test_init_creates_encrypted_store`
- Status: PASS via `PYTHONPATH=src .venv/bin/pytest -v`

### 2) profile/family/prefs CRUD works

- Evidence test: `tests/test_profile_family_commands.py::test_profile_set_and_get_roundtrip`
- Status: PASS via `PYTHONPATH=src .venv/bin/pytest -v`
- Implemented commands:
  - `profile set|get`
  - `prefs set|get`
  - `family add|list|update|remove`

### 3) context preview is selective

- Evidence tests:
  - `tests/test_context_selector.py::test_finance_question_selects_finance_fields_only`
  - `tests/test_context_preview_command.py::test_context_preview_selective_output`
- Status: PASS via `PYTHONPATH=src .venv/bin/pytest -v`

### 4) ask works with fallback when API key missing

- Evidence test: `tests/test_ask_command.py::test_generate_answer_falls_back_without_api_key`
- Status: PASS via `PYTHONPATH=src .venv/bin/pytest -v`

### 5) no plaintext sensitive file tracked by git

- Evidence test: `tests/test_gitignore_safety.py::test_gitignore_blocks_sensitive_files`
- `.gitignore` includes:
  - `*.enc`
  - `.env`
- Status: PASS via `PYTHONPATH=src .venv/bin/pytest -v`

## Verification Snapshot

- Command: `PYTHONPATH=src .venv/bin/pytest -v`
- Result: `10 passed`
- Command: `git status --short`
- Result at capture time:
  - `?? docs/plans/2026-03-02-personal-context-cli-acceptance.md`
  - `?? docs/plans/2026-03-02-personal-context-cli-implementation.md`
