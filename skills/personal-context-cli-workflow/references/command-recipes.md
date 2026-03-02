# Command Recipes

## Session Password

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

## Basic Setup

```bash
personal-context init \
  --data-file ./profile.enc
```

Expected:
- `profile.enc` exists.
- File content is encrypted bytes.

## Profile and Preferences

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

## Family CRUD

```bash
personal-context family add \
  --data-file ./profile.enc \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc
```

## Context and Ask

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

`--provider auto` uses external logged-in CLI credentials from `codex` or `claude`.
