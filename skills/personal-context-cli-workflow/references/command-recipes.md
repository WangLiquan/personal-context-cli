# Command Recipes

Use one explicit password and pass it with `--password`.

## Basic Setup

```bash
personal-context init \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

Expected:
- `profile.enc` exists.
- File content is encrypted bytes.

## Profile and Preferences

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --age 32 \
  --industry internet \
  --income-range 50-100w

personal-context prefs set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
personal-context family add \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Context and Ask

```bash
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

`--provider auto` uses external logged-in CLI credentials from `codex` or `claude`.
