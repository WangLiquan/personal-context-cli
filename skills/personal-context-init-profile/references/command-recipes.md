# Init and Profile Recipes

## Bootstrap

```bash
./skills/personal-context-init-profile/scripts/pctx.sh init \
  --data-file ./profile.enc \
  --password pass123
```

## Owner Profile

```bash
./skills/personal-context-init-profile/scripts/pctx.sh profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w
```

## Preferences

```bash
./skills/personal-context-init-profile/scripts/pctx.sh prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
./skills/personal-context-init-profile/scripts/pctx.sh family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse

./skills/personal-context-init-profile/scripts/pctx.sh family list \
  --data-file ./profile.enc \
  --password pass123
```
