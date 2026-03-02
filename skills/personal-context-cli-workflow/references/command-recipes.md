# Command Recipes

## Basic Setup

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh init \
  --data-file ./profile.enc \
  --password pass123
```

Expected:
- `profile.enc` exists.
- File content is encrypted bytes.

## Profile and Preferences

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w

./skills/personal-context-cli-workflow/scripts/pctx.sh prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse

./skills/personal-context-cli-workflow/scripts/pctx.sh family list \
  --data-file ./profile.enc \
  --password pass123
```

## Context and Ask

```bash
./skills/personal-context-cli-workflow/scripts/pctx.sh context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123

./skills/personal-context-cli-workflow/scripts/pctx.sh ask \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

Without `OPENAI_API_KEY`, `ask` prints fallback text containing selected context.
