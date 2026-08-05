# Changelog

All notable changes to `modelctl` are documented in this file.

The project follows Semantic Versioning. Until a stable `1.0.0` release, minor versions may include breaking changes with migration notes.

## [0.3.0]

Third development release in progress.

### Added

- Named configuration snapshots through `modelctl profiles save <name>`.
- Profile inspection through `modelctl profiles list` and `modelctl profiles show <name>`.
- Validated profile application through `modelctl profiles use <name>`.
- Explicit profile deletion through `modelctl profiles delete <name>`.
- Service and CLI regression tests for profile lifecycle, normalization, malformed data, and validation failures.

### Changed

- Coordinated the workspace, CLI, core, SDK, and lockfile versions at `0.3.0`.
- Marked `release.toml` as `draft` while v0.3.0 development is active.
- Applied profiles as one complete configuration snapshot instead of a hidden runtime overlay.
- Preserved unrelated configuration keys and saved profiles when applying a profile.

### Security

- Profiles contain only provider, model, launcher, and compatibility policy values.
- Credential material and launcher-managed authentication data are never included in profiles.
- Unknown or extra stored profile fields are rejected instead of being silently accepted.
- Profile application validates the complete model and launcher selection before one atomic configuration write.

## [0.2.0] - 2026-08-04

Second development release.

### Added

- Provider-aware launcher recommendations through `modelctl launchers recommend`.
- Explicit safe apply for installed recommendations.
- Persisted `warn` and `strict` compatibility policies with per-run overrides.
- Immutable launcher execution requests and explicit launcher capabilities.
- Read-only compatibility remediation plans through `modelctl launchers remediate`.
- Explicit remediation application through `modelctl launchers remediate --apply`.
- Anthropic native provider discovery and official model-catalog synchronization.
- Google Gemini native provider discovery and official model-catalog synchronization.
- OpenAI native provider discovery and official model-catalog synchronization.
- Official `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GEMINI_API_KEY`, and `OPENAI_API_KEY` aliases.
- Native routing to Claude Code, Gemini CLI, and Codex CLI.
- Primary CI provider-contract tests for Anthropic, Google, and OpenAI.

### Changed

- Coordinated all package versions at `0.2.0`.
- Preserved unknown native launcher options after `modelctl run` instead of rejecting them as modelctl options.
- Unified recommendation, compatibility diagnosis, remediation, and execution around one capability-driven request contract.
- Removed the hard-coded OpenRouter recommendation in favor of declared model translation capabilities.
- Directed compatibility warnings to preview-first remediation.
- Filtered Google models that do not support `generateContent`.
- Conservatively filtered OpenAI non-coding model families without guessing unavailable context, price, or modality data.
- Kept provider catalog credentials separate from launcher subprocess authentication.

### Fixed

- Prevented pagination request snapshots from being corrupted by reusing one mutable query dictionary.
- Added focused provider contract tests to primary CI so provider regressions cannot leave CI green while full test and release workflows fail.

### Security

- Upgraded locked `cryptography` from 49.0.0 to patched 50.0.0 for `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247`.
- Removed the need for an audit exception; `uv audit --locked` passes on the release lock.
- Preserved keyring-first credential storage, explicit plaintext fallback, private permissions, atomic writes, and symbolic-link rejection.
- Continued to pin external GitHub Actions to immutable commit SHAs.
- Kept PyPI publication and OIDC write permission disabled.

### Compatibility

- Configurations without `compatibility_policy` continue to default to `warn`.
- Strict policies stop before subprocess creation on known provider/launcher mismatches.
- `--warn-compatibility` and `--strict-compatibility` override the persisted policy for one run.
- Existing CLI commands and configuration keys remain valid.
- Aider continues to translate only OpenRouter model identifiers.
- Recommendation and remediation remain read-only unless `--apply` is explicitly provided.

## [0.1.0] - 2026-08-03

First development release.

### Added

- OpenRouter credential storage and model-catalog synchronization.
- Interactive and non-interactive provider/model selection.
- Persistent provider, model, and launcher configuration.
- Claude Code, Gemini CLI, Codex CLI, and Aider launchers.
- Native launcher argument forwarding.
- Automatic OpenRouter model translation for Aider.
- Launcher discovery, installation status, and selection commands.
- `modelctl doctor` diagnostics and compatibility feedback.
- Linux, macOS, and Windows test coverage with Python 3.13.
- Coordinated wheel and source-distribution builds for the CLI, core, and SDK packages.
- GitHub Release artifact generation with SHA-256 checksums.
- English and Korean project documentation.

### Security

- Operating-system keyring storage by default.
- Explicit plaintext fallback approval.
- Atomic private local writes and symbolic-link rejection.
- Pinned GitHub Actions and locked dependency audit.
- Validated release inputs and immutable GitHub Release assets.
- PyPI publication disabled.
