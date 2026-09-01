# modelctl Project Progress

Last updated: 2026-09-01

## Project goal

`modelctl` is a universal command-line control plane for AI models and coding agents. The long-term goal is to become the **uv of AI coding agents**: one small CLI for selecting providers and models, managing credentials and reusable configuration, and launching multiple coding-agent CLIs consistently.

Development principle:

1. Deliver a working end-to-end workflow first.
2. Add regression, cross-platform, packaging, release, security, and typing gates.
3. Refactor abstractions only after real integrations expose common requirements.

## Branch and release state

- Canonical release branch: `main`
- Ongoing development branch: `refac`
- Latest ready and published version: `0.2.0`
- Active development version: `0.3.0`
- Manifest status: `draft`
- Current phase: final documentation review and readiness preparation
- Active feature branch: `feat/v0.3.0-final-docs`
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)

The v0.2.0 tag and immutable GitHub Release were created from exact `main` commit `9da3f46fc2fe817c2643437d48f42dd078f26482` after clean audit, Ruff, tests, builds, installed-wheel smoke checks, and checksums passed.

## Completed v0.3.0 increments

### Named profiles — PR #36

- save, list, show, use, and delete named configuration snapshots
- validate provider/model and launcher selection before one atomic configuration write
- preserve unrelated settings and exclude all credentials from profiles

### Versioned launcher plugin SDK — PR #37

- public immutable `LaunchRequest`
- explicit `LauncherCapabilities`
- stable `LauncherMetadata`
- public `LauncherPlugin` protocol
- launcher contract version `1.0` with major-version compatibility validation

### Installed launcher discovery — PR #39

- discover only installed `modelctl.launchers` Python entry points
- preserve built-ins and reject built-in ID collisions before loading external code
- reject duplicate external launcher IDs deterministically
- isolate import, initialization, metadata, and contract failures
- adapt valid plugins into the existing core launcher runtime
- verify real installed entry-point discovery in isolated packaging smoke tests

PR #38 contains the same discovery implementation history but was closed unmerged after the connected GitHub draft-to-ready transition failed because of an upstream GraphQL schema incompatibility. PR #39 is the actual merged implementation path.

### Plugin diagnostics and compatibility hardening — PR #40

- make `modelctl doctor` plugin-aware
- report distribution origin, plugin ID, SDK contract compatibility, executable availability, and discovery/probe failures
- keep unrelated broken plugins isolated while escalating the selected launcher failure
- verify external plugins use recommendation, remediation, strict compatibility, immutable request, and native argument forwarding paths

### Static type-check enforcement — PR #41

- enforce strict `basedpyright` at the public SDK, named-profile, and launcher-plugin boundaries
- type profile collaborators and persisted profile narrowing explicitly
- type installed launcher entry points and discovery status
- ship PEP 561 `py.typed` markers for SDK/core and verify them from installed wheels
- repeat the strict type gate in the complete release workflow

## Final v0.3.0 scope review

The planned v0.3.0 functional scope is complete. Profile portability is explicitly deferred because no concrete usage need has been demonstrated; it is not a release blocker.

Explicit non-goals for v0.3.0 remain:

- provider plugins
- automatic plugin installation or update
- remote plugin registries
- arbitrary filesystem plugin paths
- credential export
- PyPI publication

`release.toml` remains `draft` through final documentation review and full readiness validation. Only the dedicated `main`-targeting readiness PR may switch it to `ready`.

## Stable v0.2.0 workflows

### OpenRouter through Aider

```bash
modelctl auth login openrouter
modelctl models sync openrouter
modelctl use --provider openrouter --model anthropic/claude-sonnet-4
modelctl launchers remediate --apply
modelctl config set compatibility-policy strict
modelctl doctor
modelctl run
```

### Native providers

- Anthropic catalog through Claude Code
- Google Gemini catalog through Gemini CLI
- OpenAI native catalog through Codex CLI

Provider catalog credentials remain separate from launcher authentication and are never injected from keyring storage into launcher subprocess environments.

## Remaining v0.3.0 sequence

1. Complete this final documentation and release-criteria review on `refac`.
2. Run one clean full readiness validation of the completed tree: dependency audit, Ruff, strict type check, provider contracts, all cross-platform tests, all distributions, installed-wheel/plugin smoke checks, release dry-run, and checksums.
3. Create one dedicated readiness branch from that exact validated `refac` lineage, change release metadata from `draft` to `ready`, finalize release-facing documentation, and open `main` ← readiness PR.
4. Require the `main`-targeting PR to independently pass CI, Test, Package, and Release workflows before merge.
5. After merge, allow the release workflow to revalidate the exact `main` merge commit before creating immutable tag `v0.3.0` and its GitHub Release.

## Validation commands

```bash
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run basedpyright
uv run pytest
python scripts/release_validation.py
python scripts/release_validation.py --print-status
```
