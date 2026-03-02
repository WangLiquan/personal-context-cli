---
name: personal-context-ask-flow
description: Use when running question answering in the Personal Context CLI project, including selective context preview and ask with provider relay modes.
---

# Personal Context Ask Flow

## Overview

Use this skill for question workflows only.
It focuses on `context preview` and `ask` with provider control (`auto`, `codex`, `claude`, `api`).

## Fast Path

From project root:

```bash
./skills/personal-context-ask-flow/scripts/pctx.sh --help
```

From any path:

```bash
PCTX_PROJECT_ROOT=/Users/wangliquan/Desktop/personal-context-cli \
  /Users/wangliquan/Desktop/personal-context-cli/skills/personal-context-ask-flow/scripts/pctx.sh --help
```

## Ask Workflow

### 1) Preview selected context

```bash
./skills/personal-context-ask-flow/scripts/pctx.sh context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

### 2) Ask with provider relay

```bash
./skills/personal-context-ask-flow/scripts/pctx.sh ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Provider Modes

- `auto`: try `codex` first, then `claude`, then fallback path.
- `codex`: force relay to `codex exec`.
- `claude`: force relay to `claude -p`.
- `api`: explicit API key path.

## Verification

```bash
cd /Users/wangliquan/Desktop/personal-context-cli
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
