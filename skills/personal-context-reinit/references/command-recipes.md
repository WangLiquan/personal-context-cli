# Reinit Recipes

Use the profile password explicitly with `--password`.

## One-Step Reset

```bash
personal-context init \
  --data-file ./profile.enc \
  --password "<YOUR_PASSWORD>"
```

Expected:
- Existing encrypted profile data is overwritten with default empty payload.
- User must re-enter profile, preferences, and family information.
