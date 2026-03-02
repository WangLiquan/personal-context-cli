---
name: personal-context-cli-workflow
description: Use when working with the Personal Context CLI project to initialize encrypted profile storage, update profile or family data, preview selective context, and run ask with API fallback for finance, career, education, or family decision support.
---

# Personal Context CLI Workflow

## Overview

Use this skill to operate the local Personal Context CLI quickly and consistently.
Prefer the bundled wrapper script to avoid repeated `PYTHONPATH` and interpreter setup.

## Project Assumptions

- Project root: `/Users/wangliquan/Desktop/personal-context-cli`
- Virtualenv: `.venv`
- CLI module: `personal_context_cli`

If the project root differs, set `PCTX_PROJECT_ROOT` before running commands.

## Fast Path

Run from the project root:

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh --help
```

Or from anywhere:

```bash
PCTX_PROJECT_ROOT=/Users/wangliquan/Desktop/personal-context-cli \
  /Users/wangliquan/Desktop/personal-context-cli/skills/personal-context-cli-workflow/scripts/pctx.sh --help
```

## Core Workflows

### 1) Initialize encrypted store

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh init \
  --data-file ./profile.enc \
  --password pass123
```

### 2) Maintain owner profile

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w

./skills/personal-context-cli-workflow/scripts/pctx.sh profile get \
  --data-file ./profile.enc \
  --password pass123
```

### 3) Maintain preferences and family members

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first

./skills/personal-context-cli-workflow/scripts/pctx.sh family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse \
  --age-band 30-39 \
  --occupation-or-school "product manager"
```

### 4) Preview context and ask

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123

./skills/personal-context-cli-workflow/scripts/pctx.sh ask \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Fallback Behavior

- If `OPENAI_API_KEY` is not set, `ask` returns a fallback response that includes selected context.
- If `OPENAI_API_KEY` is set, `ask` uses provider logic from `src/personal_context_cli/llm_adapter.py`.

## Verification

Run full tests before claiming success:

```bash
cd /Users/wangliquan/Desktop/personal-context-cli
PYTHONPATH=src .venv/bin/pytest -v
```

## Troubleshooting

- `No module named personal_context_cli`:
  - Use `pctx.sh` or ensure `PYTHONPATH=src`.
- `invalid choice` for command:
  - Run `pctx.sh --help` and verify subcommand path.
- `.venv/bin/python` missing:
  - Recreate venv and install dependencies.
- Wrong password or decrypt failure:
  - Verify `--password` and `--data-file` pair.

## References

For command recipes and expected outputs, read:
- `references/command-recipes.md`
