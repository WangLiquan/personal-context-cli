# Command Recipes

## Basic Setup

```bash
personal-context init \
  --data-file ./profile.enc \
  --password pass123
```

Expected:
- `profile.enc` exists.
- File content is encrypted bytes.

## Profile and Preferences

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w

personal-context prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
personal-context family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc \
  --password pass123
```

## Context and Ask

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123

personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

`--provider auto` uses external logged-in CLI credentials from `codex` or `claude`.
