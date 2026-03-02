# Init and Profile Recipes

When guiding users through init, always request a custom password input and do not provide a default-password choice.

Use one explicit password and pass it with `--password`.

## Bootstrap

```bash
personal-context init \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

## Owner Profile

```bash
personal-context profile set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --age 32 \
  --industry internet \
  --income-range 50-100w
```

## Preferences

```bash
personal-context prefs set \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --response-style brief \
  --strategy-style balanced \
  --locale-bias CN-first
```

## Family CRUD

```bash
personal-context family add \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>" \
  --relation spouse

personal-context family list \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```
