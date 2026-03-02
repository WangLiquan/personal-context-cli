# Ask Flow Recipes

## Context Preview

```bash
./skills/personal-context-ask-flow/scripts/pctx.sh context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Ask with Auto Relay

```bash
./skills/personal-context-ask-flow/scripts/pctx.sh ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Force Provider

```bash
# Force codex relay
./skills/personal-context-ask-flow/scripts/pctx.sh ask "question" \
  --provider codex \
  --data-file ./profile.enc \
  --password pass123

# Force claude relay
./skills/personal-context-ask-flow/scripts/pctx.sh ask "question" \
  --provider claude \
  --data-file ./profile.enc \
  --password pass123
```
