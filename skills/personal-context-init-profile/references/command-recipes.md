# Init and Profile Recipes

When guiding users through init, always request a custom password input and do not provide a default-password choice.

## Session Password

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

## Bootstrap

```bash
personal-context init \
  --data-file ./profile.enc
```

## Owner Profile

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --age 32 \
  --industry internet \
  --income-range 50-100w
```

## Preferences

```bash
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
