---
name: personal-context-init-profile
description: Use when initializing encrypted personal context storage or updating profile, preferences, and family records with direct `personal-context` commands.
---

# Personal Context Init Profile

## Overview

Use this skill for onboarding and profile maintenance.
All commands use the installed `personal-context` CLI directly.
Ask the user for a password before running any init/profile command.
Do not offer a default password option.
Require the user to input a custom password directly.

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

## Core Commands

### 1) Initialize encrypted store

```bash
personal-context init \
  --data-file ./profile.enc
```

### 2) Owner profile

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --age 32 \
  --industry internet \
  --income-range 50-100w

personal-context profile get \
  --data-file ./profile.enc
```

### 3) Preferences

```bash
personal-context prefs set \
  --data-file ./profile.enc \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first

personal-context prefs get \
  --data-file ./profile.enc
```

### 4) Family records

```bash
personal-context family add \
  --data-file ./profile.enc \
  --relation spouse \
  --age-band 30-39 \
  --occupation-or-school "product manager"

personal-context family list \
  --data-file ./profile.enc
```

## Verification

```bash
cd $PROJECT_ROOT
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
