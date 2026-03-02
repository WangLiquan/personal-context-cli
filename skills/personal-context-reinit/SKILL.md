---
name: personal-context-reinit
description: Use when clearing all personal-context data and restarting setup from a clean encrypted profile file.
---

# Personal Context Reinit

## Overview

Use this skill when the user wants to clear all existing personal-context settings and start over.
This workflow resets `profile.enc` to an empty encrypted payload, then requires reconfiguration.

## One-Time Install

```bash
pipx install "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.3-beta"
```

Ask for the current profile password and pass it with `--password`.

## Reinit Workflow

Ask for confirmation before running reset commands because this operation overwrites all stored profile data.

```bash
personal-context init \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

After reset, reconfigure profile, preferences, and family data with the init/profile workflows.

## Verification

```bash
cd $PROJECT_ROOT
PYTHONPATH=src .venv/bin/pytest -v
```

## References

- `references/command-recipes.md`
