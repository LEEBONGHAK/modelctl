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

`ANTHROPIC_API_KEY` can replace `modelctl auth login anthropic` for catalog synchronization. Claude Code continues to manage launcher authentication itself.

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

`MODELCTL_GOOGLE` has the highest environment precedence, followed by `GOOGLE_API_KEY` and `GEMINI_API_KEY`. Gemini CLI continues to manage launcher authentication itself.

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

`OPENAI_API_KEY` can replace `modelctl auth login openai` for catalog synchronization. Codex CLI continues to manage its own ChatGPT or API-key authentication; modelctl does not inject stored credentials into subprocess environments.

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
- Bounded Anthropic cursor pagination with fresh per-request query dictionaries
- Anthropic mapping for IDs, names, maximum input tokens, image input, and thinking capability
- Official `ANTHROPIC_API_KEY` support with `MODELCTL_ANTHROPIC` precedence
- Google Gemini native model synchronization through the official Models API
- Bounded Google page-token pagination with fresh per-request query dictionaries, repeated-token detection, and maximum-page guards
- Google model normalization for `models/<id>`, maximum input tokens, generation support, and thinking capability
- Filtering of Google models that do not support `generateContent`
- Official `GOOGLE_API_KEY` and `GEMINI_API_KEY` support with `MODELCTL_GOOGLE` precedence
- OpenAI native model synchronization through the official Models API
- Bearer authentication through `OPENAI_API_KEY` with `MODELCTL_OPENAI` precedence
- Conservative OpenAI coding-candidate filtering for GPT, o-series, and Codex IDs
- Exclusion of OpenAI embedding, image, audio, transcription, TTS, moderation, realtime, search, computer-use, deep-research, Sora, and fine-tuned IDs
- No guessed OpenAI context, pricing, or vision metadata when the model-list response does not provide those fields
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
- Native Anthropic selection resolving to Claude Code
- Native Google selection resolving to Gemini CLI
- Native OpenAI selection resolving to Codex CLI

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

### CI, packaging, and release

- Primary CI dependency audit and Ruff checks
- Primary CI provider API contract suites for Anthropic, Google, and OpenAI
- Complete pytest suite on Ubuntu, macOS, and Windows with Python 3.13
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

### CI failure history

PR #28 exposed a mutable pagination-parameter defect. The Google client reused one dictionary across page requests, causing the recorded first request to appear mutated after the second page token was inserted. Ubuntu, macOS, Windows, and the release dry-run failed consistently. The fix creates a fresh query dictionary for every request.

The failing commit still had a green primary CI and Package result because those workflows did not execute provider tests. PR #29 adds focused provider contract tests to primary CI, preserving the independent complete OS matrix and release gates while detecting provider HTTP regressions earlier.

### Documentation and security gates

- English README and complete Korean `README.ko.md`
- Bilingual Anthropic, Google, and OpenAI provider documentation
- Bilingual release guide, completion criteria, and security policy
- Per-PR English/Korean engineering records
- Locked uv workspace installation
- Full commit-SHA pinning for external GitHub Actions
- Least-privilege workflow permissions
- Security regression coverage for private files, credential fallback, untrusted tags, merged-event trust boundaries, and model synchronization
- Current dependency audit runs without an advisory exclusion

## Completed pull requests

| PR | Summary | Result |
| --- | --- | --- |
| #21 | Begin v0.2.0 with provider-aware launcher recommendations | Merged |
| #23 | Add strict compatibility execution and native option forwarding | Merged |
| #24 | Persist warn/strict compatibility policy and per-run overrides | Merged |
| #25 | Formalize launcher capabilities and immutable execution requests | Merged |
| #26 | Add preview-first compatibility remediation and explicit apply | Merged |
| #27 | Add Anthropic native model catalog and Claude Code routing | Merged |
| #28 | Add Google Gemini native model catalog and Gemini CLI routing | Merged |

## Active v0.2.0 development

- Completed launcher recommendation, strict policy, persisted policy, immutable request, and remediation increments in PRs #21–#26
- Completed Anthropic native provider catalog and Claude Code routing in PR #27
- Completed Google Gemini native provider catalog and Gemini CLI routing in PR #28
- Active OpenAI native provider catalog, Codex CLI routing, and provider CI hardening in PR #29
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
- OpenAI Models API does not expose endpoint capability, context, modality, or pricing metadata in its list response
- OpenAI coding-candidate filtering is intentionally conservative and may require maintenance as model naming evolves
- Anthropic and Google catalog APIs do not provide pricing in their responses, so synchronized prices are zero
- Google catalog vision support remains false because the Models API response does not declare input modalities
- Native launcher authentication remains owned by each launcher and is separate from modelctl catalog credentials
- Remediation currently changes only the selected launcher
- Remediation does not install software, change providers or models, or execute launchers
- Capabilities describe current provider routing but do not yet model every launcher feature or option
- Plugin-based launcher discovery is deferred
- Full static type-check enforcement is not yet a quality gate
- Local plaintext credential fallback remains unencrypted and should be used only when explicitly accepted
- The security review is source- and test-based, not an independent penetration test

## Next priorities

1. Validate and merge the OpenAI native-provider and provider-CI workflow.
2. Review whether the four proven provider implementations justify a shared HTTP catalog client helper without hiding vendor differences.
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
