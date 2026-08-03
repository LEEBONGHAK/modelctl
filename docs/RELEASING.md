# Releasing modelctl / modelctl 릴리스

This document describes coordinated development releases for the `modelctl`, `modelctl-core`, and `modelctl-sdk` Python distributions.

이 문서는 `modelctl`, `modelctl-core`, `modelctl-sdk` Python 배포물의 통합 개발 릴리스 절차를 설명합니다.

## English

### Current publication policy

- `release.toml` is the machine-readable release decision.
- A version is eligible for a tag only when its manifest status is `ready`.
- A trusted push to `refac`, or the merged event of a pull request whose base is `refac`, independently runs dependency audit, lint, tests, package builds, and installed-wheel smoke validation.
- Closed but unmerged pull requests do not run release publication.
- After all checks pass, the workflow creates the coordinated `v*` tag and one GitHub Release.
- Existing tags and GitHub Release assets are never overwritten.
- **PyPI publication is not configured and no PyPI publishing job exists.**

### Completion criteria

The complete functional, quality, security, and publication criteria are maintained in [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md).

The release manifest must match all package versions:

```toml
version = "0.1.0"
status = "ready"
channel = "development"
publish_pypi = false
```

Package versions are read from:

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

Validate locally:

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.1.0
```

Validation also requires the matching changelog entry, English and Korean READMEs, security policy, release criteria, and this release guide.

### Pull-request dry run

An opened, synchronized, or reopened relevant pull request runs the complete release validation without creating a tag or release:

- validate package versions, manifest, documentation, and proposed tag
- install the locked workspace
- run `uv audit --locked`
- run Ruff and the complete pytest suite
- build wheels and source distributions without workspace source overrides
- install the built wheels in a fresh Python 3.13 environment
- verify installed imports, `modelctl version`, and `modelctl --help`
- generate `SHA256SUMS`
- upload a temporary workflow artifact

### Creating a completed release

To mark a version complete:

1. Update the three package versions.
2. Add the matching `CHANGELOG.md` entry.
3. Update `docs/RELEASE_CRITERIA.md` for the version.
4. Set the matching version and `status = "ready"` in `release.toml`.
5. Merge the reviewed release-readiness pull request into `refac`.

The trusted merged event checks out the exact merge commit and reruns every release gate. If successful and the tag does not exist, it creates `v<version>` at that merge commit and publishes the GitHub Release with generated notes, six Python distribution files, and `SHA256SUMS`.

A direct trusted push to `refac` and a manually created matching `v*` tag are also supported. A manual tag must point to a commit contained in `refac` and passes the same full validation before a release is created.

### Trust boundaries

- The merged-event publication condition requires `pull_request.merged == true` and base branch `refac`.
- The workflow checks out `pull_request.merge_commit_sha`, not an untrusted head branch, for the post-merge release run.
- Closed but unmerged pull requests are skipped.
- Pull-request dry runs do not receive content write permission.
- Only the publication job receives `contents: write`, after all validation succeeds.

### Immutability and recovery

- An existing tag is never moved.
- Existing GitHub Release assets are never replaced.
- If a version needs correction after tagging, prepare a new patch version instead of modifying the existing release.
- If a tag exists at another commit, later release triggers skip that version rather than overwriting it.

### PyPI

PyPI publication remains intentionally deferred. Enabling it later requires a separate reviewed pull request, package-name ownership confirmation, a protected environment, Trusted Publishing configuration, and a dry-run plan. Creating a GitHub tag or Release does not publish anything to PyPI.

## 한국어

### 현재 게시 정책

- `release.toml`을 기계가 판독하는 release 결정 파일로 사용합니다.
- Manifest status가 `ready`인 버전만 tag 생성 대상이 됩니다.
- 신뢰된 `refac` push 또는 base가 `refac`인 Pull Request의 실제 병합 이벤트에서 dependency audit, lint, test, package build, 설치된 wheel smoke 검증을 독립적으로 수행합니다.
- 닫혔지만 병합되지 않은 Pull Request에서는 release 게시를 실행하지 않습니다.
- 모든 검증을 통과한 경우 통합 `v*` tag와 하나의 GitHub Release를 생성합니다.
- 기존 tag와 GitHub Release asset은 절대 덮어쓰지 않습니다.
- **PyPI 게시는 구성되어 있지 않으며 PyPI 게시 job도 존재하지 않습니다.**

### 완료 기준

전체 기능·품질·보안·게시 기준은 [`RELEASE_CRITERIA.md`](RELEASE_CRITERIA.md)에서 관리합니다.

Release manifest는 모든 package version과 일치해야 합니다.

```toml
version = "0.1.0"
status = "ready"
channel = "development"
publish_pypi = false
```

Package version은 다음 파일에서 읽습니다.

```text
apps/modelctl/pyproject.toml
packages/core/pyproject.toml
packages/sdk/pyproject.toml
```

로컬 검증 명령은 다음과 같습니다.

```bash
python scripts/release_validation.py
python scripts/release_validation.py --print-status
python scripts/release_validation.py --tag v0.1.0
```

검증에는 동일 버전의 changelog, 영문·한국어 README, 보안 정책, 완료 기준, 이 릴리스 가이드도 필요합니다.

### Pull Request dry run

관련 Pull Request가 열리거나 갱신되거나 다시 열리면 tag나 release를 생성하지 않고 전체 release 검증을 수행합니다.

- Package version, manifest, 문서, 제안 tag 검증
- Lockfile 기반 workspace 설치
- `uv audit --locked` 실행
- Ruff 및 전체 pytest suite 실행
- Workspace source override 없는 wheel·source distribution 빌드
- 새로운 Python 3.13 환경에 생성한 wheel 설치
- 설치된 package import, `modelctl version`, `modelctl --help` 검증
- `SHA256SUMS` 생성
- 임시 workflow artifact 업로드

### 완성 버전 릴리스 생성

버전을 완성 상태로 표시하는 절차는 다음과 같습니다.

1. 세 package version을 변경합니다.
2. 동일 버전의 `CHANGELOG.md` 항목을 추가합니다.
3. 해당 버전에 맞게 `docs/RELEASE_CRITERIA.md`를 갱신합니다.
4. `release.toml`에 같은 version과 `status = "ready"`를 설정합니다.
5. 검토된 release-readiness Pull Request를 `refac`에 병합합니다.

신뢰된 병합 이벤트는 정확한 merge commit을 checkout한 뒤 모든 release gate를 다시 실행합니다. 성공하고 tag가 존재하지 않으면 해당 merge commit에 `v<version>`을 생성하고 자동 release note, Python 배포 파일 여섯 개, `SHA256SUMS`를 포함한 GitHub Release를 게시합니다.

신뢰된 `refac` 직접 push와 동일 형식의 수동 `v*` tag도 지원합니다. 수동 tag는 `refac`에 포함된 commit을 가리켜야 하며 같은 전체 검증을 통과해야 합니다.

### 신뢰 경계

- 병합 이벤트 게시 조건은 `pull_request.merged == true`와 base branch `refac`을 모두 요구합니다.
- 병합 후 release 실행에서는 신뢰할 수 없는 head branch가 아니라 `pull_request.merge_commit_sha`를 checkout합니다.
- 닫혔지만 병합되지 않은 Pull Request는 건너뜁니다.
- Pull Request dry run에는 content write 권한이 없습니다.
- 모든 검증을 통과한 뒤 publication job에만 `contents: write` 권한을 부여합니다.

### 불변성 및 복구

- 기존 tag는 이동하지 않습니다.
- 기존 GitHub Release asset은 교체하지 않습니다.
- Tag 생성 이후 수정이 필요하면 기존 release를 변경하지 않고 새로운 patch version을 준비합니다.
- 같은 tag가 다른 commit에 이미 존재하면 이후 release trigger는 해당 버전을 덮어쓰지 않고 건너뜁니다.

### PyPI

PyPI 게시는 의도적으로 연기한 상태입니다. 나중에 활성화하려면 package name 소유권 확인, 보호된 environment, Trusted Publishing 설정, dry-run 계획을 포함한 별도 검토 PR이 필요합니다. GitHub tag나 Release를 생성해도 PyPI에는 아무것도 게시되지 않습니다.
