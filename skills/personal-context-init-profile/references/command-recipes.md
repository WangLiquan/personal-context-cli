# Init and Profile Recipes

## Bootstrap

```bash
personal-context init \
  --data-file ./profile.enc \
  --password pass123
```

## Owner Profile

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 \
  --industry internet \
  --income-range 50-100w
```

## Preferences

```bash
personal-context prefs set \
  --data-file ./profile.enc \
  --password pass123 \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
personal-context family add \
  --data-file ./profile.enc \
  --password pass123 \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc \
  --password pass123
```
