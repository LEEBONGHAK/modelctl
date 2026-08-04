# modelctl Project Progress

Last updated: 2026-08-04

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, and security gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Branch and release state

- Release branch: `main`
- Ongoing development branch: `refac`
- Completed release: `0.1.0` on `main`
- Coordinated development version: `0.2.0` on `refac`
- Manifest: `release.toml`
- Current status: `draft`
- Channel: development release
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)
- Notable changes: [`CHANGELOG.md`](../CHANGELOG.md)

The feature scope planned for v0.2.0 is implemented. The remaining work is release hardening and promotion: merge the patched dependency update, complete a readiness review, mark the manifest `ready`, and promote the exact validated commit to `main` for final release publication.

## Current end-to-end workflows

### OpenRouter through Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
modelctl launchers recommend
modelctl launchers remediate
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

### Anthropic through Claude Code

```bash
modelctl auth login anthropic
modelctl models sync anthropic
modelctl use --provider anthropic --model claude-opus-4-6
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

`ANTHROPIC_API_KEY` can replace stored modelctl credentials for catalog synchronization. Claude Code owns launcher authentication.

### Google Gemini through Gemini CLI

```bash
modelctl auth login google
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

Environment precedence is `MODELCTL_GOOGLE`, `GOOGLE_API_KEY`, then `GEMINI_API_KEY`. Gemini CLI owns launcher authentication.

### OpenAI through Codex CLI

```bash
modelctl auth login openai
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
modelctl launchers recommend
modelctl launchers remediate
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

`OPENAI_API_KEY` can replace stored modelctl credentials for catalog synchronization. Codex CLI owns launcher authentication.

Provider credentials stored by modelctl are not injected into launcher subprocess environments.

## Implemented v0.2.0 scope

### Provider and model workflows

- OpenRouter catalog synchronization and Aider model translation
- Anthropic native catalog synchronization and Claude Code routing
- Google Gemini native catalog synchronization and Gemini CLI routing
- OpenAI native catalog synchronization and Codex CLI routing
- Official provider environment-variable aliases with modelctl-specific precedence
- Bounded HTTP timeouts and pagination guards
- Explicit malformed-response failures
- Conservative mapping when provider catalog APIs omit capability, pricing, or modality data
- Interactive and non-interactive provider/model selection
- Persistent provider-scoped model repository

### Launcher and compatibility workflows

- Immutable `LaunchRequest` values
- Explicit `LauncherCapabilities`
- Capability-driven launcher recommendations
- Read-only recommendation and remediation previews
- Explicit safe apply that refuses unavailable launchers
- Persisted `warn` and `strict` compatibility policies
- Per-run warn/strict overrides
- Native launcher argument forwarding without shell execution
- Shared compatibility semantics across execution, diagnostics, recommendation, and remediation

### Credential and local-state security

- Operating-system keyring by default
- No silent plaintext downgrade
- Explicit plaintext fallback approval
- Private POSIX permissions
- Atomic protected-file writes
- Symbolic-link path rejection
- Credentials separated from launcher subprocess authentication

### CI, packaging, and release

- Locked dependency audit and Ruff
- Focused native-provider API contract tests in primary CI
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
- Wheel and source-distribution builds for all packages
- Isolated installed-wheel package and CLI smoke tests
- Coordinated package, manifest, changelog, documentation, and tag validation
- Independent release workflow gates and SHA-256 checksum generation
- Immutable GitHub Release behavior
- PyPI publication intentionally disabled

## CI failure history

PR #28 exposed a mutable pagination-parameter defect. The Google client reused one dictionary across page requests, so the recorded first request appeared mutated after the second page token was inserted. Ubuntu, macOS, Windows, and the release dry-run failed consistently.

PR #28 fixed the request construction by creating a fresh query dictionary for every page. PR #29 added focused Anthropic, Google, and OpenAI provider contract tests to primary CI so similar HTTP-client regressions are detected before the complete OS matrix and release workflow.

## Security readiness

Issue #22 tracked `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247` in `cryptography 49.0.0`. Upstream released patched version 50.0.0 on 2026-07-31.

PR #30 updates `uv.lock` to `cryptography 50.0.0`. The issue can be closed after the dependency audit, complete tests, packaging, and release dry-run pass and the PR is merged.

No audit exclusion is retained for this advisory.

## v0.2.0 pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #21 | Begin v0.2.0 with provider-aware launcher recommendations | Merged |
| #23 | Add strict compatibility execution and native option forwarding | Merged |
| #24 | Persist warn/strict compatibility policy and per-run overrides | Merged |
| #25 | Formalize launcher capabilities and immutable execution requests | Merged |
| #26 | Add preview-first compatibility remediation and explicit apply | Merged |
| #27 | Add Anthropic native model catalog and Claude Code routing | Merged |
| #28 | Add Google Gemini native model catalog and Gemini CLI routing | Merged |
| #29 | Add OpenAI native model catalog, Codex routing, and provider CI hardening | Merged |
| #30 | Upgrade `cryptography` to patched 50.0.0 and close issue #22 | Active |

## Remaining steps to complete v0.2.0

1. Merge PR #30 after all security and release-dry-run checks pass.
2. Close issue #22 with the merged commit and validation evidence.
3. Run a release-readiness audit against the exact latest `refac` commit.
4. Finalize PR #30 history, release criteria, README status, changelog release wording, and progress documentation.
5. Change `release.toml` from `status = "draft"` to `status = "ready"` in a dedicated readiness PR.
6. Merge the reviewed readiness change into `main` and require the release workflow to independently pass audit, lint, 137+ tests, builds, installed-wheel smoke checks, metadata validation, and checksum generation.
7. Confirm immutable tag `v0.2.0` and the GitHub Release assets. PyPI remains disabled.

## Deferred work after v0.2.0

- Shared provider HTTP helpers only where four integrations demonstrate genuinely identical behavior
- Additional remediation actions only when they are safe, reversible, and previewable
- Profile management with a complete tested workflow
- Plugin-based launcher discovery
- Full static type-check enforcement
- Separately reviewed PyPI Trusted Publishing milestone

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
uv build packages/core --out-dir dist --no-sources
uv build packages/sdk --out-dir dist --no-sources
uv build apps/modelctl --out-dir dist --no-sources
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
```
