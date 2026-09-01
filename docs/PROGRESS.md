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
- Development branch: `refac`
- Ready version: `0.3.0`
- Manifest status: `ready`
- Current phase: dedicated readiness promotion to `main`
- Readiness branch: `release/v0.3.0-readiness`
- Validated `refac` baseline commit: `1b5639a699dc3e26e53a61ad8a9ee1dcb4933e03`
- Validated baseline tree: `aaad179a59b5f6b98e8319ff4c2b3818d84d392e`
- PyPI publication: disabled
- Completion criteria: [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)

The v0.2.0 tag and immutable GitHub Release were created from exact `main` commit `9da3f46fc2fe817c2643437d48f42dd078f26482`. Version 0.3.0 is now a validated readiness candidate awaiting promotion of its dedicated readiness branch to `main`.

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

### Final documentation and scope review — PR #42

- reconcile English/Korean release documentation with the completed v0.3.0 feature set
- resolve profile portability as an explicitly deferred, evidence-driven follow-up rather than a release blocker
- preserve the exact `Draft` release-validation contract through final documentation review
- complete full CI, Package, Test, and Release validation with no unresolved review threads

## Readiness validation evidence

The final PR #42 head `1e82ccf819f14fad3b6d6f2a986f0247703b632e` passed CI, Package, Test, and complete Release validation. Its Git tree is `aaad179a59b5f6b98e8319ff4c2b3818d84d392e`.

After PR #42 merged, exact `refac` commit `1b5639a699dc3e26e53a61ad8a9ee1dcb4933e03` retained that identical tree. The merge commit independently passed push CI, Package, and the full Python 3.13 test matrix on Ubuntu, macOS, and Windows.

The readiness branch was created directly from that exact baseline commit. Its changes are limited to release-state and release-facing documentation finalization; no runtime feature is added.

## Final v0.3.0 scope

Profile portability is explicitly deferred because no concrete usage need has been demonstrated. It is not a v0.3.0 release blocker.

Explicit non-goals remain:

- provider plugins
- automatic plugin installation or update
- remote plugin registries
- arbitrary filesystem plugin paths
- credential export
- PyPI publication

## Release path

1. Open the dedicated `main` ← `release/v0.3.0-readiness` pull request.
2. Require that exact readiness head to pass CI, Test, Package, and complete Release validation.
3. Merge only the validated readiness head into `main`.
4. Let the release workflow independently revalidate the exact `main` merge commit before creating immutable tag `v0.3.0` and its GitHub Release.
5. Never overwrite an existing tag or release asset; PyPI publication remains disabled.

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
