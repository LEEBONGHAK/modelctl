# Changelog

All notable changes to `modelctl` are documented in this file.

The project follows Semantic Versioning. Until a stable `1.0.0` release, minor versions may include breaking changes with migration notes.

## [0.2.0]

Draft development release.

### Added

- Provider-aware launcher recommendations through `modelctl launchers recommend`.
- Explicit `--apply` support that selects only an installed recommended launcher.
- Opt-in strict compatibility enforcement through `modelctl run --strict-compatibility`.
- Persisted compatibility policy configuration through `modelctl config set compatibility-policy <warn|strict>`.
- Per-run warning override through `modelctl run --warn-compatibility`.
- Immutable launcher execution requests that carry model, provider, and native arguments together.
- Explicit launcher capabilities for native-provider support and provider model translation.
- Read-only compatibility remediation plans through `modelctl launchers remediate`.
- Explicit remediation application through `modelctl launchers remediate --apply`.
- Anthropic native provider discovery and official model-catalog synchronization.
- Official `ANTHROPIC_API_KEY` environment-variable support.
- Bounded Anthropic Models API pagination with malformed-response and cursor guards.
- Google Gemini native provider discovery and official model-catalog synchronization.
- Official `GOOGLE_API_KEY` and `GEMINI_API_KEY` environment-variable support.
- Bounded Gemini Models API pagination with malformed-response and repeated-token guards.
- OpenAI native provider discovery and official model-catalog synchronization.
- Official `OPENAI_API_KEY` environment-variable support.
- Primary CI provider-contract tests for Anthropic, Google, and OpenAI integrations.

### Changed

- Began the v0.2.0 development cycle with coordinated package version `0.2.0` and release status `draft`.
- Preserved unknown native launcher options after `modelctl run` instead of treating them as modelctl parsing errors.
- `modelctl run` now resolves the persisted compatibility policy when no command-line override is supplied.
- Launcher recommendation, compatibility diagnosis, and execution now share one capability-driven request contract.
- OpenRouter launcher recommendation no longer depends on a hard-coded launcher ID.
- Compatibility warnings now direct users to preview or explicitly apply a capability-driven remediation plan.
- Anthropic provider selection now resolves to the existing native Claude Code launcher for recommendation and remediation.
- Google provider selection now resolves to the existing native Gemini CLI launcher for recommendation and remediation.
- Google catalog synchronization excludes models that do not support `generateContent`.
- OpenAI provider selection now resolves to the existing native Codex CLI launcher for recommendation and remediation.
- OpenAI catalog synchronization conservatively excludes non-coding model families and fields unavailable from the Models API response are not guessed.

### Fixed

- Prevented provider pagination request snapshots from being corrupted by reuse of one mutable query dictionary.
- Added provider API contract tests to the primary CI workflow so provider regressions cannot leave CI green while the OS test matrix and release dry-run fail.

### Security

- Upgraded the locked `cryptography` dependency from 49.0.0 to patched version 50.0.0 for `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247`.
- Dependency audit runs without retaining an exception for the patched advisory.

### Compatibility

- Existing launcher execution still supports configurations without provider context; recommendations require an explicit provider and model selection.
- Configurations without `compatibility_policy` continue to use the backward-compatible `warn` behavior.
- Strict policies stop before subprocess execution on known provider/launcher mismatches, while `--warn-compatibility` can override a persisted strict policy for one run.
- Invalid persisted compatibility policies fail explicitly instead of silently changing execution behavior.
- The launcher execution-contract refactor does not change CLI commands, configuration keys, subprocess argument order, or Aider OpenRouter model translation.
- Remediation preview never changes configuration; apply changes only the selected launcher and refuses unavailable recommendations.
- `MODELCTL_ANTHROPIC` keeps precedence over the official `ANTHROPIC_API_KEY` alias.
- `MODELCTL_GOOGLE` keeps precedence over official aliases; `GOOGLE_API_KEY` takes precedence over `GEMINI_API_KEY`.
- `MODELCTL_OPENAI` keeps precedence over the official `OPENAI_API_KEY` alias.
- Provider credentials managed by modelctl are used for catalog synchronization and are not injected into launcher subprocess environments.

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
- Trusted merged-PR release validation against the exact `refac` merge commit.
- English and Korean project documentation.

### Security

- Operating-system keyring storage is the default credential backend.
- Plaintext credential fallback requires explicit user approval.
- Configuration and fallback credentials use atomic writes and private POSIX permissions.
- Protected local files reject symbolic-link paths.
- GitHub Actions dependencies are pinned to immutable commit SHAs.
- Release-tag input is validated before use in shell commands or workflow outputs.
- Closed but unmerged pull requests cannot publish releases.
- Locked dependencies are audited in CI.

### Fixed

- Unified authentication and model synchronization on one credential service.
- Repaired model synchronization dependency wiring and credential conversion.
- Removed duplicate and unused placeholder services.
- Aligned the repository's `main` branch with `refac` so default-branch workflow events use the current validated release policy.

### Known limitations

- PyPI publication is intentionally disabled.
- OpenRouter automation is currently provided through Aider; native launchers may require their own provider credentials or proxy configuration.
- Plugin discovery and profile management remain future work.
