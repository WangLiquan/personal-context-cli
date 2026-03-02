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

Use one explicit password for this profile and pass it with `--password` in each command.

## Core Commands

### 1) Initialize encrypted store

```bash
personal-context init \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

### 2) Owner profile

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --age 32 \
  --industry internet \
  --income-range 50-100w

personal-context profile get \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

### 3) Preferences

```bash
personal-context prefs set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first

personal-context prefs get \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

### 4) Family records

```bash
personal-context family add \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --relation spouse \
  --age-band 30-39 \
  --occupation-or-school "product manager"

personal-context family list \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Verification

```bash
cd $PROJECT_ROOT
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
