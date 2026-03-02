# Contributing

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install pytest pydantic cryptography httpx
```

## Development Flow

1. Create a feature branch from `main`.
2. Follow test-first workflow for new features and fixes.
3. Run tests before committing:
   - `PYTHONPATH=src .venv/bin/pytest -v`
4. Keep commits focused and atomic.

## Safety Rules

- Never commit real personal data.
- Keep `*.enc` and `.env` local.
- Prefer templates (`.env.example`, `profile.example.json`) for shared examples.
