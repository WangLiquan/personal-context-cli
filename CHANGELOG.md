# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] - 2026-03-02

### Added
- Local-first encrypted personal context CLI workflows for `init`, `profile`, `prefs`, `family`, `context`, and `ask`.
- Skill packages for direct usage in OpenX/Claude Code:
  - `personal-context-cli-workflow`
  - `personal-context-init-profile`
  - `personal-context-ask-flow`
  - `personal-context-reinit`
- Ask follow-up flow for missing context, with encrypted persistence to local storage.
- Ask history persistence and profile fact-memory extraction (for long-lived key facts such as mortgage/income/risk preference).
- Chinese README (`README.zh-CN.md`).

### Changed
- `ask` workflow now favors concise, relevant context windows instead of replaying all historical notes.
- Documentation now recommends host-auth relay usage (Codex/Claude CLI login) over project API key setup.

### Fixed
- Auto relay mode now allows `claude` provider under `CLAUDECODE` environments.
- Skill docs updated to avoid requiring manual question-type classification in ask workflows.
- Init skill flow updated to require custom password input (no default-password option in skill guidance).
