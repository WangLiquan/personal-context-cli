# Ask Flow Recipes

## Context Preview

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Ask with Auto Relay

```bash
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Force Provider

```bash
# Force codex relay
personal-context ask "question" \
  --provider codex \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password pass123

# Force claude relay
personal-context ask "question" \
  --provider claude \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password pass123
```
