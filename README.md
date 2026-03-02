# Personal Context CLI

Plugin-first personal context system for Claude Code / OpenX.
Store personal and family context locally with encryption, then use skills for daily ask workflows.

English | [简体中文](README.zh-CN.md)

## Project Intent

Most users should treat this project as a skill/plugin package, not a script project.

- Primary interaction: call installed skills in Claude Code / OpenX.
- CLI commands are the underlying engine and are mainly for setup/troubleshooting.
- Data is encrypted at rest in your local `profile.enc`.

## What Problems This Solves

- Personal context gets lost between sessions, so assistants give generic answers.
- Sensitive profile data is hard to reuse safely across questions.
- Raw conversation logs become noisy and hurt answer quality over time.

This project keeps context local and encrypted, then structures it into:
- `ask_history` for full traceability
- `fact_memory` for long-lived key facts
- compact retrieval context for better answer accuracy

## Plugin-First Quick Start

### 1) Install CLI runtime once

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@main"
```

If you need a pinned stable tag instead of `main`, use `v1.0` (`v1.0.0`).

```bash
pipx install --force "git+https://github.com/WangLiquan/personal-context-cli.git@v1.0.0"
```

### 2) Install skills once

```bash
npx skills add WangLiquan/personal-context-cli -g --all -y
```

### 3) Use skills in Claude Code / OpenX

Call these by name in chat:
- `personal-context-cli-workflow`
- `personal-context-init-profile`
- `personal-context-ask-flow`
- `personal-context-reinit`

Typical flow:
- First setup profile: `personal-context-init-profile`
- Ask daily questions: `personal-context-ask-flow`
- Reset and start over: `personal-context-reinit`

## Password Input

- Password is set/confirmed in your init flow.
- No environment-variable setup is required.
- In direct CLI usage, pass the password explicitly with `--password`.

## How Ask Persistence Works

- Every `ask` question is persisted to local encrypted `ask_history`.
- Key long-lived facts are extracted into `owner_profile.fact_memory` (for example, mortgage/income/risk preference).
- Model context uses a compact relevant window (`fact_memory` + recent notes) to reduce noise.
- Missing context can still trigger a follow-up question, and that answer is also persisted.

## Relay Providers

- `auto` (default): try logged-in `codex` / `claude` relays
- `codex`: force `codex exec`
- `claude`: force `claude -p`

If you see relay unavailable, verify at least one CLI is installed and logged in:
- `codex`
- `claude`

## Direct CLI (Advanced / Debug)

```bash
personal-context init --data-file ./profile.enc --password "<YOUR_PASSWORD>"
personal-context profile set --data-file ./profile.enc --password "<YOUR_PASSWORD>" --age 32 --industry internet --income-range 50-100w
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Security Model

- Data is encrypted at rest before writing to disk.
- Real data files (`*.enc`) and `.env` are ignored by git.
- Password is passed at runtime via `--password` (or interactive prompt).
- This repository should store code and templates only.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install pytest
PYTHONPATH=src .venv/bin/pytest -v
```
