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
- Manifest status: `ready`
- Channel: development release
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)
- Release procedure: [`RELEASING.md`](RELEASING.md)

PR #31 promoted the validated v0.2.0 lineage to `main` as `d8f2bad5111e18859c746acc412ce1ea0d627e05`. A publication recovery run then exposed one final readiness discrepancy: the patched lock used `cryptography 50.0.0`, but the obsolete audit ignore entry remained in workspace configuration.

PR #33 removes that stale exception and adds a release-validation gate that rejects non-empty audit ignore lists for any `ready` release.

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
- Dependency audit without an advisory exclusion or ignore warning
- Ready-release validation rejects non-empty audit ignore lists
- Pinned external GitHub Actions and least-privilege workflow permissions
- PyPI publishing and OIDC write permission absent

### Quality and release gates

- Primary CI audit, Ruff, and provider contract suites
- Complete 138-test suite on Ubuntu, macOS, and Windows with Python 3.13
- All wheel and source-distribution builds
- Isolated installed-wheel import and CLI smoke tests
- Package, manifest, changelog, documentation, clean-audit policy, and tag validation
- Independent release-workflow verification
- SHA-256 checksums and immutable GitHub Release behavior

## CI and release findings

PR #28 exposed mutable pagination parameters that changed a recorded first request after a second-page token was added. PR #29 added focused native-provider contract suites to primary CI.

PR #32 successfully reran every release gate against the exact `main` commit but failed before tag creation because its shell logic treated a 404 JSON response as an existing tag SHA. That failed run also exposed the stale audit ignore warning. No tag or release was created or overwritten.

PR #33 fixes the audit policy itself before publication is attempted again. The final publication recovery must use the new PR #33 `main` merge commit and corrected empty-tag handling.

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
| #31 | v0.2.0 readiness declaration and `main` promotion | Merged |
| #32 | Guarded publication recovery trigger | Failed safely; no tag created |
| #33 | Remove stale audit ignore and enforce clean ready releases | Active |

## Remaining completion steps

1. Merge PR #33 after all four workflows pass on its final documented head.
2. Target the resulting exact `main` merge commit in the guarded publication recovery.
3. Rerun release metadata validation, clean dependency audit, Ruff, all 138 tests, builds, isolated wheel smoke tests, and checksums.
4. Create and verify immutable tag `v0.2.0` plus one GitHub Release containing three wheels, three source distributions, and `SHA256SUMS`.
5. Close the unmerged recovery PR after publication and remove its one-time workflow from the recovery branch.

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
