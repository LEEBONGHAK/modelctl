# Releasing modelctl / modelctl 릴리스

This document describes coordinated development releases for the `modelctl`, `modelctl-core`, and `modelctl-sdk` Python distributions.

이 문서는 `modelctl`, `modelctl-core`, `modelctl-sdk` Python 배포물의 통합 개발 릴리스 절차를 설명합니다.

## English

### Branch policy

- `refac` is the ongoing development branch.
- `main` is the canonical completed-version and release branch.
- A completed version is promoted through a reviewed release pull request targeting `main`.
- Tags and GitHub Releases are created only from validated commits contained in `main`.

### Current v0.3.0 decision

```toml
version = "0.3.0"
status = "ready"
channel = "development"
publish_pypi = false
```

All three package versions match `0.3.0`. The readiness lineage includes PR #43 and publisher hardening in PR #44.

### Publication policy

- `release.toml` is the machine-readable release decision.
- A version is eligible for a tag only when status is `ready`.
- Ready-release validation rejects non-empty `[tool.uv.audit].ignore` entries.
- A trusted `main` push or an actually merged pull request targeting `main` independently runs audit, lint, tests, package builds, installed-wheel smoke validation, and checksums.
- Closed but unmerged pull requests cannot publish.
- The workflow creates the coordinated `v*` tag and one GitHub Release only after every gate succeeds.
- Existing tags and GitHub Release assets are never overwritten.
- **PyPI publication is not configured and no PyPI publishing job exists.**

### Validation

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.3.0
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run basedpyright
uv run pytest
```

Validation requires matching package versions, manifest, changelog, English and Korean READMEs, security policy, release criteria, this release guide, and a clean ready-release audit policy.

### Pull-request dry run

An opened, synchronized, or reopened relevant pull request performs the complete release validation without creating a tag or release:

- validate package versions, manifest, documentation, clean audit policy, and proposed tag
- install the locked workspace
- run dependency audit without an advisory exclusion or ignore warning
- run Ruff and the complete test suite
- build wheels and source distributions without workspace source overrides
- install built wheels in a fresh Python 3.13 environment
- verify imports, `modelctl version`, and `modelctl --help`
- generate `SHA256SUMS`
- upload a temporary workflow artifact

### Completing v0.3.0

1. Keep the release target based on the exact validated `main` lineage.
2. Require a clean ready-release audit policy and all completion documents.
3. Require all pull-request workflows to pass.
4. Merge the final security correction into `main` with the exact checked head SHA.
5. Run publication against that exact `main` merge commit and repeat every gate.
6. Confirm immutable tag `v0.3.0`, six Python distribution files, and `SHA256SUMS` in the GitHub Release.

### Trust boundaries

- Publication requires a validated commit contained in `main`.
- Post-merge validation checks out the exact merge commit rather than an untrusted head branch.
- Pull-request dry runs normally have read-only content permission.
- Only an explicitly reviewed publication job receives `contents: write` after validation.
- Manual matching tags must point to a commit contained in `main`.

### Immutability and recovery

- Existing tags are never moved.
- Existing GitHub Release assets are never replaced.
- A correction after tagging requires a new patch version.
- If `v0.3.0` already points elsewhere, publication fails without overwriting it.

### PyPI

PyPI publication remains intentionally deferred. Enabling it requires a separate reviewed pull request, package-name ownership confirmation, protected environment, Trusted Publishing configuration, and a dry-run plan. A GitHub tag or Release does not publish to PyPI.

## 한국어

### 브랜치 정책

- `refac`은 지속적인 개발 branch입니다.
- `main`은 완성 버전과 릴리스의 공식 branch입니다.
- 완성 버전은 `main` 대상의 검토된 release Pull Request로 승격합니다.
- Tag와 GitHub Release는 `main`에 포함된 검증 commit에서만 생성합니다.

### 현재 v0.3.0 결정

```toml
version = "0.3.0"
status = "ready"
channel = "development"
publish_pypi = false
```

세 package version은 모두 `0.3.0`입니다. Readiness 계보에는 PR #43과 PR #44의 publisher 보완이 포함됩니다.

### 게시 정책

- `release.toml`을 기계 판독 가능한 release 결정 파일로 사용합니다.
- Status가 `ready`인 버전만 tag 생성 대상입니다.
- Ready release 검증은 비어 있지 않은 `[tool.uv.audit].ignore` 항목을 거부합니다.
- 신뢰된 `main` push 또는 실제로 병합된 `main` 대상 Pull Request에서 audit, lint, test, package build, 설치 wheel smoke 검증, checksum을 독립적으로 실행합니다.
- 닫혔지만 병합되지 않은 Pull Request는 게시할 수 없습니다.
- 모든 gate가 성공한 뒤에만 통합 `v*` tag와 하나의 GitHub Release를 생성합니다.
- 기존 tag와 GitHub Release asset은 덮어쓰지 않습니다.
- **PyPI 게시는 구성되어 있지 않으며 PyPI 게시 job도 없습니다.**

### 검증

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.3.0
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run basedpyright
uv run pytest
```

검증에는 package version, manifest, changelog, 영문·한국어 README, 보안 정책, 완료 기준, release guide, clean ready-release audit policy의 일치가 필요합니다.

### Pull Request dry run

관련 Pull Request가 열리거나 갱신되거나 다시 열리면 tag나 release를 만들지 않고 전체 검증을 수행합니다.

- Package version, manifest, 문서, clean audit policy, 제안 tag 검증
- 잠긴 workspace 설치
- Advisory 예외와 ignore 경고가 없는 dependency audit
- Ruff와 전체 테스트
- Workspace source override 없는 wheel·source distribution build
- 새로운 Python 3.13 환경에 wheel 설치
- Import, `modelctl version`, `modelctl --help` 검증
- `SHA256SUMS` 생성
- 임시 workflow artifact 업로드

### v0.3.0 완료 절차

1. Release target을 정확히 검증된 `main` 계보로 유지합니다.
2. Clean ready-release audit policy와 모든 완료 문서를 요구합니다.
3. 모든 Pull Request workflow 통과를 요구합니다.
4. 확인한 head SHA 그대로 최종 보안 수정을 `main`에 병합합니다.
5. 정확한 `main` merge commit에서 게시를 실행하고 모든 gate를 다시 수행합니다.
6. 불변 tag `v0.3.0`, Python 배포 파일 여섯 개, `SHA256SUMS`가 GitHub Release에 존재하는지 확인합니다.

### 신뢰 경계

- 게시는 `main`에 포함된 검증 commit을 요구합니다.
- 병합 후 검증은 신뢰할 수 없는 head가 아니라 정확한 merge commit을 checkout합니다.
- 일반 Pull Request dry-run에는 read-only content 권한만 있습니다.
- 명시적으로 검토된 게시 job에만 검증 후 `contents: write`를 부여합니다.
- 수동 tag는 `main`에 포함된 commit을 가리켜야 합니다.

### 불변성과 복구

- 기존 tag는 이동하지 않습니다.
- 기존 GitHub Release asset은 교체하지 않습니다.
- Tag 이후 수정은 새로운 patch version으로 처리합니다.
- `v0.3.0`이 다른 commit을 가리키면 덮어쓰지 않고 실패 처리합니다.

### PyPI

PyPI 게시는 의도적으로 연기했습니다. 활성화하려면 package name 소유권, 보호 environment, Trusted Publishing, dry-run 계획을 포함한 별도 검토 PR이 필요합니다. GitHub tag나 Release는 PyPI 게시를 수행하지 않습니다.

## Publisher recovery / 게시 복구

- Both publication workflows call `scripts/publish_release.py` and share a per-tag concurrency group with `cancel-in-progress: false`.
- Only HTTP 404 means a tag or published Release is absent. Authentication, rate-limit, server, malformed-response, and transport failures stop publication.
- A tag-creation conflict is re-read and accepted only when it resolves to the exact validated target commit, including annotated tags.
- Releases are created as drafts. All six distributions and `SHA256SUMS` are downloaded and verified before publishing, then verified again after publication.
- A completed release retry verifies the existing bundle against its own checksums without replacing assets; a complete draft can be verified and published.
- An incomplete or corrupt release fails visibly. Inspect the retained draft and original run artifacts; never move the tag or automatically replace assets. Corrections to a tagged version require a new patch version under the immutability policy.
- `workflow_dispatch` is validation-only. Its tag input does not change the checked-out commit; select the intended ref. A recovery publication must validate the exact tagged commit, not a later `main` commit with the same version.
- The `/release` path checks out the requested merged PR commit and repeats audit, lint, strict type checks, tests, builds, installed typing-marker checks, and checksums. The selected commit must contain the shared publisher.

두 게시 경로는 공통 publisher와 태그별 동시 실행 제어를 사용합니다. 404만 부재로 판단하며 다른 조회 오류는 실패 처리합니다. 태그 생성 충돌은 정확한 대상 commit을 재확인합니다. Release는 초안으로 만들고 배포 파일 6개와 체크섬을 내려받아 검증한 후 공개합니다. 재실행 시 기존 파일을 교체하지 않고 검증하며, 불완전한 초안은 공개하지 않습니다. 수동 workflow 실행은 검증 전용이며, 게시 복구에는 태그가 가리키는 정확한 commit을 다시 검증해야 합니다.
