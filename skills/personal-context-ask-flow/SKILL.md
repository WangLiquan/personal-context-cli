---
name: personal-context-ask-flow
description: Use when running question answering in the Personal Context CLI project, including selective context preview and ask with host-auth relay providers.
---

# Personal Context Ask Flow

## Overview

Use this skill for question workflows only.
It focuses on `context preview` and `ask` with provider control (`auto`, `codex`, `claude`).

## One-Time Install

```bash
pipx install "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.1-beta"
```

## Ask Workflow

### 1) Preview selected context

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

### 2) Ask with provider relay

```bash
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Provider Modes

- `auto`: try `codex` first, then `claude`, then host-auth guidance.
- `codex`: force relay to `codex exec`.
- `claude`: force relay to `claude -p`.

## Verification

```bash
cd /Users/wangliquan/Desktop/personal-context-cli
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
