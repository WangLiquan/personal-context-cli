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

## Core Commands

```bash
# initialize encrypted store
personal-context init \
  --data-file ./profile.enc \
  --password pass123

# set and get profile
personal-context profile set \
  --data-file ./profile.enc \
  --password pass123 \
  --age 32 --industry internet --income-range 50-100w

personal-context profile get \
  --data-file ./profile.enc \
  --password pass123

# selective context preview
personal-context context preview \
  "Should I increase my emergency fund?" \
  --type finance \
  --data-file ./profile.enc \
  --password pass123

# ask with host-auth relay (no project API key)
personal-context ask \
  "Should I increase my emergency fund?" \
  --provider auto \
  --relay-timeout-seconds 45 \
  --relay-retries 1 \
  --type finance \
  --data-file ./profile.enc \
  --password pass123
```

## Provider Modes

- `auto` (default): use logged-in `codex`/`claude` relay
- `codex`: force `codex exec` relay
- `claude`: force `claude -p` relay

## Security Model

- Data is encrypted at rest before writing to disk.
- Real data files (`*.enc`) and `.env` are ignored by git.
- This repository should store code and templates only.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install pytest
PYTHONPATH=src .venv/bin/pytest -v
```
