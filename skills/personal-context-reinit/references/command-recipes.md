# Reinit Recipes

## Session Password

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

## One-Step Reset

```bash
personal-context init \
  --data-file ./profile.enc
```

Expected:
- Existing encrypted profile data is overwritten with default empty payload.
- User must re-enter profile, preferences, and family information.
