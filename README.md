# Personal Context CLI

Local-first Python CLI for encrypted personal/family context and targeted Q&A.

## Quickstart

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install pytest pydantic cryptography httpx
```

## Core Commands

```bash
# initialize encrypted store
PYTHONPATH=src .venv/bin/python -m personal_context_cli init \
  --data-file ./profile.enc \
  --password pass123

# set and get profile
PYTHONPATH=src .venv/bin/python -m personal_context_cli profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 --industry internet --income-range 50-100w

PYTHONPATH=src .venv/bin/python -m personal_context_cli profile get \
  --data-file ./profile.enc \
  --password pass123

# selective context preview
PYTHONPATH=src .venv/bin/python -m personal_context_cli context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123

# ask with fallback (when no OPENAI_API_KEY)
PYTHONPATH=src .venv/bin/python -m personal_context_cli ask \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Security Model

- Data is encrypted at rest before writing to disk.
- Real data files (`*.enc`) and `.env` are ignored by git.
- This repository should store code and templates only.

## Tests

```bash
PYTHONPATH=src .venv/bin/pytest -v
```

## Agent Skill

This repository includes an agent skill:

- `skills/personal-context-cli-workflow/`

Use the bundled wrapper script to avoid repeating runtime setup:

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh --help
```
