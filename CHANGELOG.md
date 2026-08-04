# Changelog

All notable changes to `modelctl` are documented in this file.

The project follows Semantic Versioning. Until a stable `1.0.0` release, minor versions may include breaking changes with migration notes.

## [0.2.0]

Draft development release.

### Added

- Provider-aware launcher recommendations through `modelctl launchers recommend`.
- Explicit `--apply` support that selects only an installed recommended launcher.
- Opt-in strict compatibility enforcement through `modelctl run --strict-compatibility`.

### Changed

- Began the v0.2.0 development cycle with coordinated package version `0.2.0` and release status `draft`.
- Preserved unknown native launcher options after `modelctl run` instead of treating them as modelctl parsing errors.

### Compatibility

- Existing launcher execution still supports configurations without provider context; recommendations require an explicit provider and model selection.
- Default runs continue to warn without blocking, while strict runs stop before subprocess execution on known provider/launcher mismatches.

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
