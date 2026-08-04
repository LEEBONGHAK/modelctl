# Releasing modelctl / modelctl 릴리스

This document describes coordinated development releases for the `modelctl`, `modelctl-core`, and `modelctl-sdk` Python distributions.

이 문서는 `modelctl`, `modelctl-core`, `modelctl-sdk` Python 배포물의 통합 개발 릴리스 절차를 설명합니다.

## English

### Branch policy

- `refac` is the ongoing development branch.
- `main` is the canonical completed-version and release branch.
- A completed version is promoted through a reviewed release pull request targeting `main`.
- Tags and GitHub Releases are created only from validated commits contained in `main`.

### Current v0.2.0 decision

```toml
version = "0.2.0"
status = "ready"
channel = "development"
publish_pypi = false
```

All three package versions match `0.2.0`. The readiness branch descends from the exact validated `refac` merge commit that includes PR #30 and `cryptography 50.0.0`.

### Publication policy

- `release.toml` is the machine-readable release decision.
- A version is eligible for a tag only when status is `ready`.
- A trusted `main` push or an actually merged pull request targeting `main` independently runs audit, lint, tests, package builds, installed-wheel smoke validation, and checksums.
- Closed but unmerged pull requests cannot publish.
- The workflow creates the coordinated `v*` tag and one GitHub Release only after every gate succeeds.
- Existing tags and GitHub Release assets are never overwritten.
- **PyPI publication is not configured and no PyPI publishing job exists.**

### Validation

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

Validation requires matching package versions, manifest, changelog, English and Korean READMEs, security policy, release criteria, and this release guide.

### Pull-request dry run

An opened, synchronized, or reopened relevant pull request performs the complete release validation without creating a tag or release:

- validate package versions, manifest, documentation, and proposed tag
- install the locked workspace
- run dependency audit without an advisory exclusion
- run Ruff and all 137 tests
- build wheels and source distributions without workspace source overrides
- install built wheels in a fresh Python 3.13 environment
- verify imports, `modelctl version`, and `modelctl --help`
- generate `SHA256SUMS`
- upload a temporary workflow artifact

### Completing v0.2.0

1. Keep the readiness branch based on the exact validated `refac` lineage.
2. Set `status = "ready"` and update completion documents.
3. Open the reviewed readiness pull request against `main`.
4. Require all pull-request workflows to pass.
5. Merge into `main` with the exact checked head SHA.
6. Confirm that the post-merge release run checks out the `main` merge commit and reruns every gate.
7. Confirm immutable tag `v0.2.0`, six Python distribution files, and `SHA256SUMS` in the GitHub Release.

If the platform does not emit the expected merged-pull-request publication event, the repository owner can use the existing audited `/release v0.2.0` command on the merged readiness pull request. That fallback resolves the exact merge commit, requires it to belong to `main`, and reruns the same gates before publication.

### Trust boundaries

- Publication requires `pull_request.merged == true` and base branch `main`, a trusted `main` push, or the owner-only validated fallback.
- Post-merge validation checks out the exact merge commit rather than the untrusted head branch.
- Pull-request dry runs have read-only content permission.
- Only the final publication job receives `contents: write` after validation.
- Manual matching tags must point to a commit contained in `main`.

### Immutability and recovery

- Existing tags are never moved.
- Existing GitHub Release assets are never replaced.
- A correction after tagging requires a new patch version.
- If `v0.2.0` already points elsewhere, publication exits without overwriting it.

### PyPI

PyPI publication remains intentionally deferred. Enabling it requires a separate reviewed pull request, package-name ownership confirmation, protected environment, Trusted Publishing configuration, and a dry-run plan. A GitHub tag or Release does not publish to PyPI.

## 한국어

### 브랜치 정책

- `refac`은 지속적인 개발 branch입니다.
- `main`은 완성 버전과 릴리스의 공식 branch입니다.
- 완성 버전은 `main` 대상의 검토된 release Pull Request로 승격합니다.
- Tag와 GitHub Release는 `main`에 포함된 검증 commit에서만 생성합니다.

### 현재 v0.2.0 결정

```toml
version = "0.2.0"
status = "ready"
channel = "development"
publish_pypi = false
```

세 package version은 모두 `0.2.0`입니다. Readiness branch는 PR #30과 `cryptography 50.0.0`을 포함한 정확한 검증 `refac` merge commit에서 파생됐습니다.

### 게시 정책

- `release.toml`을 기계 판독 가능한 release 결정 파일로 사용합니다.
- Status가 `ready`인 버전만 tag 생성 대상입니다.
- 신뢰된 `main` push 또는 실제로 병합된 `main` 대상 Pull Request에서 audit, lint, test, package build, 설치 wheel smoke 검증, checksum을 독립적으로 실행합니다.
- 닫혔지만 병합되지 않은 Pull Request는 게시할 수 없습니다.
- 모든 gate가 성공한 뒤에만 통합 `v*` tag와 하나의 GitHub Release를 생성합니다.
- 기존 tag와 GitHub Release asset은 덮어쓰지 않습니다.
- **PyPI 게시는 구성되어 있지 않으며 PyPI 게시 job도 없습니다.**

### 검증

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.2.0
uv sync --all-packages --locked
uv audit --locked
uv run ruff check .
uv run pytest
```

검증에는 package version, manifest, changelog, 영문·한국어 README, 보안 정책, 완료 기준, 이 release guide의 일치가 필요합니다.

### Pull Request dry run

관련 Pull Request가 열리거나 갱신되거나 다시 열리면 tag나 release를 만들지 않고 전체 검증을 수행합니다.

- Package version, manifest, 문서, 제안 tag 검증
- 잠긴 workspace 설치
- Advisory 예외 없는 dependency audit
- Ruff와 전체 137개 테스트
- Workspace source override 없는 wheel·source distribution build
- 새로운 Python 3.13 환경에 wheel 설치
- Import, `modelctl version`, `modelctl --help` 검증
- `SHA256SUMS` 생성
- 임시 workflow artifact 업로드

### v0.2.0 완료 절차

1. Readiness branch를 정확히 검증된 `refac` 계보에서 유지합니다.
2. `status = "ready"`와 완료 문서를 갱신합니다.
3. `main` 대상 readiness Pull Request를 엽니다.
4. 모든 Pull Request workflow 통과를 요구합니다.
5. 확인한 head SHA 그대로 `main`에 병합합니다.
6. 병합 후 release run이 `main` merge commit을 checkout하고 모든 gate를 다시 실행하는지 확인합니다.
7. 불변 tag `v0.2.0`, Python 배포 파일 여섯 개, `SHA256SUMS`가 GitHub Release에 존재하는지 확인합니다.

플랫폼이 기대한 병합 PR 게시 이벤트를 생성하지 않으면 저장소 owner가 병합된 readiness PR에 기존 `/release v0.2.0` 명령을 사용할 수 있습니다. 이 fallback은 정확한 merge commit이 `main`에 포함됐는지 확인하고 동일한 gate를 다시 실행한 뒤 게시합니다.

### 신뢰 경계

- 게시는 `pull_request.merged == true`와 base `main`, 신뢰된 `main` push, 또는 owner-only 검증 fallback을 요구합니다.
- 병합 후 검증은 신뢰할 수 없는 head가 아니라 정확한 merge commit을 checkout합니다.
- Pull Request dry-run에는 read-only content 권한만 있습니다.
- 모든 검증 후 최종 게시 job에만 `contents: write`를 부여합니다.
- 수동 tag는 `main`에 포함된 commit을 가리켜야 합니다.

### 불변성과 복구

- 기존 tag는 이동하지 않습니다.
- 기존 GitHub Release asset은 교체하지 않습니다.
- Tag 이후 수정은 새로운 patch version으로 처리합니다.
- `v0.2.0`이 다른 commit을 가리키면 덮어쓰지 않고 게시를 종료합니다.

### PyPI

PyPI 게시는 의도적으로 연기했습니다. 활성화하려면 package name 소유권, 보호 environment, Trusted Publishing, dry-run 계획을 포함한 별도 검토 PR이 필요합니다. GitHub tag나 Release는 PyPI 게시를 수행하지 않습니다.
