# Ask Flow Recipes

Use one explicit password and pass it with `--password`.

## Context Preview

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Ask with Auto Relay

```bash
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Force Provider

```bash
# Force codex relay
personal-context ask "question" \
  --provider codex \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"

# Force claude relay
personal-context ask "question" \
  --provider claude \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```
