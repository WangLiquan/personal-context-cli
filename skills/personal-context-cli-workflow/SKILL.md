---
name: personal-context-cli-workflow
description: Use when working with Personal Context CLI via direct `personal-context` commands to initialize encrypted profile storage, update profile or family data, preview selective context, and run ask with host-auth relay.
---

# Personal Context CLI Workflow

## Overview

Use this skill to operate Personal Context CLI with direct commands.
Do not rely on local wrapper scripts.

## One-Time Install

```bash
pipx install "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.1-beta"
```

## Password Session (recommended)

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

## Core Workflows

### 1) Initialize encrypted store

```bash
personal-context init \
  --data-file ./profile.enc
```

### 2) Maintain owner profile and preferences

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --age 32 \
  --industry internet \
  --income-range 50-100w

personal-context prefs set \
  --data-file ./profile.enc \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

### 3) Maintain family members

```bash
personal-context family add \
  --data-file ./profile.enc \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc
```

### 4) Preview context and ask

For ask workflows, do not ask users to classify the question type or provide structured type parameters.

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc

personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc
```

## Provider Modes

- `auto` (default): try `codex` first, then `claude`
- `codex`: force relay to `codex exec`
- `claude`: force relay to `claude -p`

## Troubleshooting

- `personal-context: command not found`:
  - Ensure `pipx` bin path is in `PATH`.
- relay timeout:
  - Increase `--relay-timeout-seconds` to 45 or 60.
- decrypt failure:
  - Verify `PCTX_PASSWORD` and `--data-file` pair.

## Verification

```bash
cd $PROJECT_ROOT
PYTHONPATH=src .venv/bin/pytest -v
```

## References

For command recipes and expected outputs, read:
- `references/command-recipes.md`
