# Personal Context CLI Design

**Date:** 2026-03-02  
**Owner:** wangliquan  
**Status:** Approved

## 1. Goal

Build a local-first Python CLI project that stores encrypted personal/family profile data and uses it to generate targeted answers for questions and decisions.  
Roadmap: local CLI first, Feishu integration later, then multi-family-member support.

## 2. Constraints and Priorities

- No UI in v1 (CLI only).
- Open source on GitHub, license MIT.
- Real personal data must never be committed.
- Local encrypted storage with a user password.
- Context usage should be selective by question type (not full-profile dump).
- v1 should include both:
  - profile/family data management
  - built-in Q&A via model API

## 3. Architecture

### 3.1 Modules

- `cli`: command parsing and user-facing commands.
- `secure_store`: password-based encryption/decryption and persistence.
- `profile_domain`: schemas, validation, and domain models.
- `context_selector`: question-type classification and relevant-field extraction.
- `llm_adapter`: provider abstraction and model invocation.
- `feishu_adapter` (future): integrate Feishu without breaking existing local design.

### 3.2 High-Level Flow

1. User runs CLI command.
2. CLI unlocks encrypted store with password.
3. Data is loaded into validated domain models.
4. For `ask`, selector extracts only relevant fields.
5. LLM adapter generates answer from question + selected context.
6. CLI returns recommendation + used-field summary + next actions.

## 4. Data Model (Encrypted Single Store)

- `owner_profile`
  - age
  - industry
  - income_range
  - city
  - career_stage
  - risk_preference
  - goals
- `family_members[]`
  - id
  - relation
  - age_band
  - occupation_or_school
  - focus_areas (health, education, retirement, etc.)
  - shared_financial_responsibilities
- `preferences`
  - response_style (brief/detailed)
  - strategy_style (conservative/balanced/aggressive)
  - locale_bias (e.g., CN-first)
- `history` (optional, can be disabled)
  - discussion summaries and decision records

## 5. Security and Open-Source Hygiene

### 5.1 Local Encryption

- Set master password at initialization.
- Derive key via KDF (`scrypt`).
- Encrypt/decrypt using authenticated symmetric encryption (`Fernet` / AES-GCM equivalent behavior).
- Keep plaintext in memory only during command execution.
- Write only encrypted bytes to disk.

### 5.2 GitHub Safety

- Commit code/docs/templates only.
- Ignore real data files:
  - `*.enc`
  - `.env`
  - other local secret paths
- Provide safe templates:
  - `.env.example`
  - `profile.example.json`
- Add a pre-commit guard to prevent accidental secret file commits.

## 6. CLI Commands (v1)

- `init`: initialize local config + encrypted store, set password.
- `profile set/get`: maintain owner profile fields.
- `family add/list/update/remove`: manage family members.
- `prefs set/get`: maintain response preferences.
- `ask "<question>" [--type career|finance|family|health|education|other]`: run targeted Q&A.
- `context preview "<question>"`: preview selected context fields only.
- `password change`: rotate master password.

## 7. Ask Pipeline

1. Decrypt and load profile data.
2. Detect/receive question type.
3. Select relevant fields only.
4. Build prompt with:
   - user question
   - selected structured context
   - response preferences
5. Call model API.
6. Return:
   - recommendation
   - fields used
   - actionable next steps

Fallback when no API key:
- return generated targeted prompt/context packet so user can use external model manually.

## 8. Error Handling

- Wrong password: clear error message, no stack dump by default.
- Corrupted encrypted file: safe diagnostics + restore guidance.
- Missing key profile fields: explain gaps and suggest exact fill commands.
- API errors/timeouts: fallback to context-only output mode.

## 9. Testing Strategy

- Unit tests:
  - encryption/decryption
  - schema validation
  - context selection rules
- Integration tests:
  - `init -> profile set -> ask`
  - use mocked LLM adapter
- Security checks:
  - no plaintext artifact on disk
  - sensitive files are ignored by git patterns

## 10. Release and Docs

- `LICENSE`: MIT
- `README.md`: setup, security model, quickstart, commands
- `SECURITY.md`: threat model and safe usage guidelines
- `CONTRIBUTING.md`: local dev/test flow

## 11. Future Roadmap

1. Feishu adapter with same domain and context-selector interfaces.
2. Family collaboration permissions (role-based sharing).
3. Optional local database backend for larger history/query use cases.
