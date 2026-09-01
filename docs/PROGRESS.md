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
- Active feature branch: `feat/v0.3.0-static-type-check`
- Active pull request: #41
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

## Current v0.3.0 increment: static type-check enforcement

PR #41 turns the existing `basedpyright` development dependency into an enforced quality gate.

### Strict boundary scope

Primary CI runs `uv run basedpyright` in strict mode over:

- public `modelctl_sdk` launcher contract and exports
- core launcher base
- installed plugin discovery
- plugin adapter and launcher registry
- named profile service

The scope is intentionally boundary-first rather than a whole-repository annotation rewrite. New v0.3 boundary code is expected to remain compatible with this strict gate.

### Boundary hardening

- Profile selection and launcher collaborators use structural Protocols instead of implicit `Any`.
- Stored profile dictionaries are narrowed only after runtime object/key validation.
- Installed Python entry points use explicit `EntryPoint` typing and discovery status literals.
- Plugin metadata/capability runtime validation remains intact while satisfying strict static checking.
- SDK/core wheels ship PEP 561 `py.typed` markers and packaging smoke tests verify the markers after isolated installation.
- Release validation repeats the same strict basedpyright gate so release paths cannot bypass primary CI typing.

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

1. Validate real profile usage and add portability only if a concrete need is demonstrated.
2. Review the complete v0.3.0 documentation and release criteria.
3. Run the final clean audit, strict type check, cross-platform tests, builds, installed-wheel/plugin smoke checks, and checksums.
4. Complete a dedicated readiness review before promotion to `main`.

Explicit non-goals remain provider plugins, automatic plugin installation, remote registries, arbitrary filesystem plugin paths, credential export, and PyPI publication during feature development.

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
