# Personal Context CLI

Local-first CLI for encrypted personal/family context and targeted Q&A.

## Install (Tester Path)

### 1) Install CLI once

```bash
pipx install "git+https://github.com/WangLiquan/personal-context-cli.git@v0.1.1-beta"
```

After this, you can run `personal-context` directly.

### 2) Install skills once (no wrapper scripts)

```bash
npx skills add WangLiquan/personal-context-cli -g --all -y
```

Then call skills by name directly in OpenX/Claude Code:
- `personal-context-cli-workflow`
- `personal-context-init-profile`
- `personal-context-ask-flow`

## Password Setup (recommended)

```bash
# write once to macOS Keychain
security add-generic-password -a "$USER" -s personal-context-cli -w "your-strong-password" -U

# load into current shell session
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

Optional: add this line to `~/.zshrc` for auto-load on new terminals.

```bash
export PCTX_PASSWORD="$(security find-generic-password -a "$USER" -s personal-context-cli -w 2>/dev/null)"
```

All subsequent commands can omit `--password`.

## Core Commands

```bash
# initialize encrypted store
personal-context init \
  --data-file ./profile.enc

# set and get profile
personal-context profile set \
  --data-file ./profile.enc \
  --age 32 --industry internet --income-range 50-100w

personal-context profile get \
  --data-file ./profile.enc

# selective context preview
personal-context context preview \
  "Should I increase my emergency fund?" \
  --data-file ./profile.enc

# ask with host-auth relay (no project API key)
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --data-file ./profile.enc
```

## Provider Modes

- `auto` (default): use logged-in `codex`/`claude` relay
- `codex`: force `codex exec` relay
- `claude`: force `claude -p` relay

## Security Model

- Data is encrypted at rest before writing to disk.
- Real data files (`*.enc`) and `.env` are ignored by git.
- Password can be passed via `--password` or session env `PCTX_PASSWORD`.
- This repository should store code and templates only.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install pytest
PYTHONPATH=src .venv/bin/pytest -v
```
