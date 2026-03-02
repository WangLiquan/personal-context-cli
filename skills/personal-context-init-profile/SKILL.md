---
name: personal-context-init-profile
description: Use when initializing encrypted personal context storage or updating profile, preferences, and family records in the Personal Context CLI project.
---

# Personal Context Init Profile

## Overview

Use this skill for onboarding and profile maintenance.
It covers encrypted store setup plus owner profile, preferences, and family CRUD commands.

## Fast Path

From project root:

```bash
./skills/personal-context-init-profile/scripts/pctx.sh --help
```

From any path:

```bash
PCTX_PROJECT_ROOT=/Users/wangliquan/Desktop/personal-context-cli \
  /Users/wangliquan/Desktop/personal-context-cli/skills/personal-context-init-profile/scripts/pctx.sh --help
```

## Core Commands

### 1) Initialize encrypted store

```bash
./skills/personal-context-init-profile/scripts/pctx.sh init \
  --data-file ./profile.enc \
  --password pass123
```

### 2) Owner profile

```bash
./skills/personal-context-init-profile/scripts/pctx.sh profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w

./skills/personal-context-init-profile/scripts/pctx.sh profile get \
  --data-file ./profile.enc \
  --password pass123
```

### 3) Preferences

```bash
./skills/personal-context-init-profile/scripts/pctx.sh prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first

./skills/personal-context-init-profile/scripts/pctx.sh prefs get \
  --data-file ./profile.enc \
  --password pass123
```

### 4) Family records

```bash
./skills/personal-context-init-profile/scripts/pctx.sh family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse \
  --age-band 30-39 \
  --occupation-or-school "product manager"

./skills/personal-context-init-profile/scripts/pctx.sh family list \
  --data-file ./profile.enc \
  --password pass123
```

## Verification

```bash
cd /Users/wangliquan/Desktop/personal-context-cli
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
