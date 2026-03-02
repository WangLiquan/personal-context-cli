# Ask Flow Recipes

## Session Password

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

## Context Preview

```bash
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc
```

## Ask with Auto Relay

```bash
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc
```

## Force Provider

```bash
# Force codex relay
personal-context ask "question" \
  --provider codex \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc

# Force claude relay
personal-context ask "question" \
  --provider claude \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc
```
