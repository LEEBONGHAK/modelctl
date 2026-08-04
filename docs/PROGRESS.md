# modelctl Project Progress

Last updated: 2026-08-04

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, and security gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Branch and release state

- Canonical release branch: `main`
- Ongoing development branch: `refac`
- Completed release on `main`: `0.1.0`
- Ready version: `0.2.0`
- Readiness branch: `release/v0.2.0-readiness`
- Manifest status: `ready`
- Channel: development release
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)
- Release procedure: [`RELEASING.md`](RELEASING.md)

The planned v0.2.0 feature and security scope is complete. The readiness branch is based on exact `refac` merge commit `1fb85812b5aca2232ac2fb479e35f38d837bb229`, which includes the patched dependency update from PR #30.

## End-to-end workflows

### OpenRouter through Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
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
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

### Google Gemini through Gemini CLI

```bash
modelctl auth login google
modelctl models sync google
modelctl use --provider google --model gemini-3.5-flash
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

### OpenAI through Codex CLI

```bash
modelctl auth login openai
modelctl models sync openai
modelctl use --provider openai --model gpt-5.6
modelctl launchers recommend
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

Provider catalog credentials remain separate from launcher authentication and are not injected from keyring storage into subprocess environments.

## Completed v0.2.0 scope

### Providers and models

- OpenRouter synchronization and Aider translation
- Anthropic native synchronization and Claude Code routing
- Google Gemini native synchronization and Gemini CLI routing
- OpenAI native synchronization and Codex CLI routing
- Official provider environment aliases with modelctl-specific precedence
- Bounded HTTP timeouts and pagination guards
- Explicit malformed-response handling
- Conservative mapping when catalog APIs omit context, price, capability, or modality fields
- Interactive and non-interactive provider/model selection

### Launchers and compatibility

- Immutable `LaunchRequest`
- Explicit `LauncherCapabilities`
- Capability-driven recommendation
- Preview-first remediation with explicit safe apply
- Refusal before mutation when a recommendation is unavailable
- Persisted `warn` and `strict` policies
- Per-run compatibility overrides
- Native argument forwarding without shell execution
- Shared semantics across execution, doctor, recommendation, and remediation

### Security

- Keyring-first credentials and no silent plaintext downgrade
- Explicit fallback approval, private permissions, atomic writes, and symlink rejection
- Provider credentials separated from coding-agent authentication
- `cryptography 50.0.0` locked for `GHSA-g6cj-pr64-35w5` / `CVE-2026-69247`
- Issue #22 closed after complete validation
- Dependency audit without a retained advisory exclusion
- Pinned external GitHub Actions and least-privilege workflow permissions
- PyPI publishing and OIDC write permission absent

### Quality and release gates

- Primary CI audit, Ruff, and provider contract suites
- Complete 137-test suite on Ubuntu, macOS, and Windows with Python 3.13
- All wheel and source-distribution builds
- Isolated installed-wheel import and CLI smoke tests
- Package, manifest, changelog, documentation, and tag validation
- Independent release-workflow verification
- SHA-256 checksums and immutable GitHub Release behavior

## CI failure resolution

PR #28 exposed mutable pagination parameters that changed a recorded first request after a second-page token was added. The defect reproduced on every operating system and in the release dry-run.

PR #28 switched to fresh per-request dictionaries. PR #29 added focused native-provider contract suites to primary CI so similar HTTP-client regressions are detected earlier while the full matrix and release workflow remain independent gates.

## v0.2.0 pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #21 | Provider-aware launcher recommendations | Merged |
| #23 | Strict compatibility and native option forwarding | Merged |
| #24 | Persisted warn/strict policy | Merged |
| #25 | Immutable execution contract and launcher capabilities | Merged |
| #26 | Preview-first compatibility remediation | Merged |
| #27 | Anthropic catalog and Claude Code routing | Merged |
| #28 | Google Gemini catalog and Gemini CLI routing | Merged |
| #29 | OpenAI catalog, Codex routing, and provider CI | Merged |
| #30 | Patched cryptography lock and issue #22 closure | Merged |
| #31 | v0.2.0 readiness declaration and `main` promotion | Active |

## Remaining completion steps

1. Require all pull-request checks on PR #31 to pass against `main`.
2. Merge the exact checked readiness head into `main`.
3. Require the post-merge release workflow to repeat audit, Ruff, all tests, builds, installed-wheel smoke checks, metadata validation, and checksum generation on the exact merge commit.
4. Confirm immutable tag `v0.2.0` and the GitHub Release containing six Python distributions plus `SHA256SUMS`.
5. Use the owner-only `/release v0.2.0` fallback only if the platform does not emit the expected merged-pull-request publication event.

PyPI remains disabled throughout this process.

## Deferred after v0.2.0

- Shared provider HTTP helpers only for proven identical behavior
- Additional safe, reversible, previewable remediation actions
- Tested profile management and plugin-based launcher discovery
- Static type-check enforcement as a separate quality milestone
- Separately reviewed PyPI Trusted Publishing

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
```
