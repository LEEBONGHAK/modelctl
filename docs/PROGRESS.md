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
- Status: `draft`
- Channel: development release
- PyPI: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)
- Notable changes: [`CHANGELOG.md`](../CHANGELOG.md)

Draft status prevents publication while v0.2.0 is under development. After an explicit readiness review, a reviewed pull request merged into `main`, or a trusted direct `main` push, creates the version tag and GitHub Release only after the release workflow independently passes dependency audit, Ruff, the complete pytest suite, distribution builds, installed-wheel smoke tests, and checksum generation.

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

`ANTHROPIC_API_KEY` can replace `modelctl auth login anthropic` for catalog synchronization. Claude Code continues to manage launcher authentication itself; modelctl does not inject stored credentials into subprocess environments.

One-run policy override with native launcher arguments:

```bash
modelctl run --strict-compatibility --sandbox workspace-write
modelctl run --warn-compatibility --continue
```

Local state defaults:

```text
~/.config/modelctl/config.json
~/.config/modelctl/credentials.json   # explicit plaintext fallback only
~/.local/share/modelctl/modelctl.db
```

## Implemented features

### Provider, model, credentials, and configuration

- Provider discovery and registry
- OpenRouter model synchronization with credential validation and bounded HTTP timeouts
- Anthropic native model synchronization through the official Models API
- Bounded Anthropic cursor pagination with page-size, repeated-cursor, and maximum-page guards
- Anthropic model mapping for IDs, names, maximum input tokens, image input, and thinking capability
- Official `ANTHROPIC_API_KEY` support with `MODELCTL_ANTHROPIC` precedence
- Persistent model repository and provider-scoped lookup
- Interactive and non-interactive provider/model selection
- Validation of registered providers and synchronized models
- Favorite-model support
- Persistent provider, model, launcher, and compatibility-policy defaults
- Validated `warn` and `strict` compatibility policy values
- Environment-variable and operating-system keyring lookup
- Keyring-first credential storage with no silent plaintext downgrade
- Explicit `--allow-plaintext-fallback`
- Provider-ID and empty-token validation
- Atomic configuration and fallback-credential writes
- Symbolic-link rejection for protected files
- POSIX private directory/file permissions (`0700` / `0600`)
- Shared credential service for authentication, diagnostics, and synchronization

### Coding-agent launchers

| Launcher ID | CLI | Native provider | Model invocation |
| --- | --- | --- | --- |
| `claude` | Claude Code | Anthropic | `claude --model <model>` |
| `gemini` | Gemini CLI | Google | `gemini --model <model>` |
| `codex` | Codex CLI | OpenAI | `codex --model <model>` |
| `aider` | Aider | Multiple providers | `aider --model <model>` |

All launchers forward native arguments as subprocess argument lists without shell execution. Aider translates OpenRouter model IDs to `openrouter/<provider>/<model>`.

The runtime contract models proven behavior explicitly:

- Immutable `LaunchRequest` containing model, provider, and native arguments
- `LauncherCapabilities` declaring native-provider affinity, provider-agnostic acceptance, and translated providers
- Capability-driven recommendations instead of hard-coded launcher IDs
- Shared request semantics across execution, compatibility policy, doctor diagnostics, and remediation planning
- Native Anthropic selection resolving to Claude Code through declared capabilities

### Management, diagnostics, and compatibility

- `modelctl launchers list`
- `modelctl launchers recommend [--apply]`
- `modelctl launchers remediate [--apply]`
- `modelctl launchers use <launcher-id>`
- Installation-state and active-launcher display
- Provider-aware recommendation of translating launchers and matching native launchers
- Read-only recommendation inspection and explicit apply that refuses unavailable launchers
- Read-only remediation plans for known active-launcher mismatches
- Explicit remediation apply that changes only the selected launcher
- No-op remediation result when no known compatibility change is required
- `modelctl doctor`
- Configuration, provider, credential, model, launcher, compatibility, and database checks
- Backward-compatible `warn` policy when no compatibility setting exists
- Persisted `warn` or `strict` policy through `modelctl config set compatibility-policy`
- Strict policy stops before subprocess execution on known mismatches
- `--strict-compatibility` and `--warn-compatibility` per-run overrides
- Explicit failure for invalid persisted policy values
- Native launcher options preserved even when they begin with `--`

### Packaging and release

- Coordinated wheel and source-distribution builds for `modelctl`, `modelctl-core`, and `modelctl-sdk`
- Workspace source overrides disabled for release builds
- Fresh-environment installed-wheel import and CLI smoke tests
- Coordinated package, manifest, changelog, documentation, and tag validation
- Machine-readable readiness status in `release.toml`
- Validation that manually tagged commits belong to `main`
- Release workflow-owned dependency audit, lint, complete tests, build, smoke test, and checksum gates
- Automatic tag creation only from successful trusted `main` changes marked `ready`
- Trusted merged-PR validation against the exact `main` merge commit
- Immutable GitHub Release creation with distributions and `SHA256SUMS`
- Existing tags and release assets are never overwritten
- PyPI publication intentionally disabled

### Documentation and security gates

- English README and complete Korean `README.ko.md`
- Bilingual Anthropic provider documentation
- Bilingual release guide, completion criteria, and security policy
- Per-PR English/Korean engineering records
- Locked uv workspace installation
- Ruff and `uv audit --locked`
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
- Full commit-SHA pinning for external GitHub Actions
- Least-privilege workflow permissions
- Security regression coverage for private files, credential fallback, untrusted tags, merged-event trust boundaries, and model synchronization
- Narrow temporary audit exception for `GHSA-g6cj-pr64-35w5`, tracked by issue #22 until the fixed dependency is published

## Completed pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #1 | Make top-level `use` and `run` executable; repair wiring | Merged |
| #2 | Stabilize workspace installation, lint, and test collection | Merged |
| #3 | Complete Claude Code execution and argument forwarding | Merged |
| #4 | Add Gemini CLI and repair runtime configuration | Merged |
| #5 | Add Codex CLI launcher | Merged |
| #6 | Add provider-aware Aider launcher | Merged |
| #7 | Add launcher listing and selection | Merged |
| #8 | Record project progress and rewrite README | Merged |
| #9 | Add `modelctl doctor` | Merged |
| #10 | Add provider/model/launcher compatibility feedback | Merged |
| #11 | Add non-interactive provider and model selection | Merged |
| #12 | Add Linux, macOS, and Windows test matrix | Merged |
| #13 | Build distributions and smoke-test installed wheels | Merged |
| #14 | Add bilingual records for PRs #1–#13 | Merged |
| #15 | Validate release tags and automate GitHub Release creation | Merged |
| #16 | Harden credentials, local state, workflows, and Korean documentation | Merged |
| #17 | Define v0.1.0 readiness and complete release gates | Merged |
| #18 | Add trusted merged-PR release publication path | Merged |
| #19 | Promote completed v0.1.0 to `main` | Merged |
| #20 | Add an owner-only fully validated release command | Merged |
| #21 | Begin v0.2.0 with provider-aware launcher recommendations | Merged |
| #23 | Add strict compatibility execution and native option forwarding | Merged |
| #24 | Persist warn/strict compatibility policy and per-run overrides | Merged |
| #25 | Formalize launcher capabilities and immutable execution requests | Merged |
| #26 | Add preview-first compatibility remediation and explicit apply | Merged |

## Active v0.2.0 development

- Completed first increment: provider-aware launcher recommendation and explicit safe apply in PR #21
- Completed second increment: strict compatibility execution and reliable native option forwarding in PR #23
- Completed third increment: persisted compatibility policy and per-run warn/strict overrides in PR #24
- Completed fourth increment: immutable launch requests and explicit launcher capabilities in PR #25
- Completed fifth increment: preview-first compatibility remediation and explicit safe apply in PR #26
- Active sixth increment: Anthropic native provider catalog and Claude Code routing in PR #27
- Version state: coordinated `0.2.0`, `status = "draft"`, PyPI disabled
- Security guarantee: modelctl provider credentials are not silently copied into launcher subprocess environments

## Architecture snapshot

```text
apps/modelctl/       Typer CLI application
packages/core/       configuration, credentials, providers, repositories, services, launchers
packages/sdk/        public SDK package foundation
scripts/             release validation helpers
tests/               regression, integration, packaging, and security tests
docs/                project, provider, release, security, and PR documentation
```

```text
Typer command
  -> application Container
  -> ProviderRegistry / ModelService
  -> provider API client + UniversalModel mapper
  -> model repository
  -> LauncherService
  -> immutable LaunchRequest + LauncherCapabilities
  -> recommendation / compatibility / remediation decision
  -> external CLI
```

## Known limitations and deferred work

- No PyPI publication
- Supported catalog providers are currently OpenRouter and Anthropic
- Anthropic Models API pricing is not available in the catalog response, so synchronized prices are zero
- Claude Code authentication remains owned by Claude Code and is separate from modelctl catalog credentials
- Remediation currently changes only the selected launcher
- Remediation does not install software, change providers or models, or execute launchers
- Capabilities describe current provider routing but do not yet model every launcher feature or option
- Plugin-based launcher discovery is deferred
- Full static type-check enforcement is not yet a quality gate
- Local plaintext credential fallback remains unencrypted and should be used only when explicitly accepted
- The security review is source- and test-based, not an independent penetration test

## Next priorities

1. Validate and merge the Anthropic native-provider workflow.
2. Evaluate Google or OpenAI native catalog integration using the same provider contract.
3. Extend remediation only when another safe, reversible action has a proven user workflow.
4. Reintroduce profile management only with a complete user workflow and tests.
5. Plan a separate reviewed PyPI publication milestone when ownership and Trusted Publishing are ready.

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
